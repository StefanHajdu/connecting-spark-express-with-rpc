<script lang="ts">
import { Card, Dropdown, DropdownItem, DropdownDivider, Button, Spinner } from "flowbite-svelte";
import { DotsHorizontalOutline, ChevronDownOutline, TrashBinOutline } from "flowbite-svelte-icons";
import { fetchSparkApi } from "$lib/clientApi";
import { syncNodeColsOnRemove } from "$lib/utils";
import { type SparkTransformResponse } from "$lib/dtype";
import { actionState, requestAction, finishAction } from "$lib/actionState.svelte";
import { nodeFactoryMethod } from "./NodeInstance";
import LoadNode from "./LoadNode.svelte";
import AddColumnNode from "./AddColumn/AddColumnNode.svelte";

let { nodesInAnalysis = $bindable(), nodeIndex, analysiId } = $props();

let nextNodeId = $state("");
let dropdownOpen = $state(false);
let summarizePromise = $state(
  Promise.resolve({
    session_id: analysiId,
    msg: "",
    columns: "",
    schema: "",
    count: -1,
  }),
);

$effect(() => {
  if (nextNodeId !== "") {
    let el = document.getElementById(nextNodeId);
    el?.scrollIntoView({ behavior: "smooth", block: "end" });
  }
});

function insertNextNode(nodeType: string) {
  let nextNode = nodeFactoryMethod(nodeType, nodesInAnalysis[nodeIndex].colsInDf);
  nodesInAnalysis = nodesInAnalysis.toSpliced(nodeIndex + 1, 0, nextNode);
  nextNodeId = nextNode.uuid;
  dropdownOpen = false;
}

async function removeNode() {
  let transformResponse: SparkTransformResponse = await fetchSparkApi("removeNode", {
    session_id: analysiId,
    node_id: nodesInAnalysis[nodeIndex].uuid,
  });
  if (transformResponse) {
    syncNodeColsOnRemove(nodesInAnalysis, nodeIndex);
    nodesInAnalysis.splice(nodeIndex, 1);
  }
}

function previewEvent() {
  requestAction(analysiId, nodesInAnalysis[nodeIndex].colsInDf, nodesInAnalysis[nodeIndex].uuid, "preview");
}

function summarizeEvent() {
  requestAction(analysiId, nodesInAnalysis[nodeIndex].colsInDf, nodesInAnalysis[nodeIndex].uuid, "sum");
  if (actionState.confirmed) {
    summarizePromise = fetchSparkApi("summarize", {
      session_id: analysiId,
      node_id: nodesInAnalysis[nodeIndex].uuid,
    });
    finishAction();
  }
}

// $inspect(`node: ${nodesInAnalysis[nodeIndex].uuid.slice(-5)}:`, nodesInAnalysis[nodeIndex].colsInDf, nodeIndex);
</script>

<div class="flex min-w-80 justify-center" id={nodesInAnalysis[nodeIndex].uuid}>
  <Card class="max-w-5xl">
    <div class="flex justify-end">
      <DotsHorizontalOutline />
      <Dropdown class="w-36">
        {#if nodesInAnalysis[nodeIndex].nodeType !== "load"}
          <div class="flex items-stretch">
            <DropdownItem onclick={removeNode} class="flex items-center">
              <TrashBinOutline class="mr-2" />
              Remove
            </DropdownItem>
          </div>
        {/if}
      </Dropdown>
    </div>
    <div class="mb-4 flex items-center justify-between">
      <p>id: {nodesInAnalysis[nodeIndex].uuid.slice(-5)}</p>
      <p>type: {nodesInAnalysis[nodeIndex].nodeType}</p>
    </div>

    {#if nodesInAnalysis[nodeIndex].title === "Load"}<LoadNode
        bind:nodesInAnalysis={nodesInAnalysis}
        nodeIndex={nodeIndex}
        analysiId={analysiId} />
    {:else if nodesInAnalysis[nodeIndex].title === "Add Column"}<AddColumnNode
        bind:nodesInAnalysis={nodesInAnalysis}
        nodeIndex={nodeIndex}
        analysiId={analysiId} />
    {/if}

    <div class="mt-2">
      <Button size="xs" color="light" on:click={previewEvent}>Preview</Button>
      <Button size="xs" color="light" on:click={summarizeEvent}>Summarize</Button>
    </div>

    {#await summarizePromise}
      <Spinner size={6} />
    {:then summarizeResponse}
      {#if summarizeResponse.count >= 0}
        <p>{summarizeResponse.count}</p>
      {/if}
    {/await}
  </Card>
</div>
<div class="p-1 mb-4 flex justify-center">
  <Button size="xs" color="dark">New Node<ChevronDownOutline class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
  <Dropdown bind:open={dropdownOpen}>
    <DropdownItem onclick={() => insertNextNode("Filter")}>Filter</DropdownItem>
    <DropdownItem onclick={() => insertNextNode("Add Column")}>Add Column</DropdownItem>
    <DropdownItem onclick={() => insertNextNode("Join")}>Join</DropdownItem>
    <DropdownDivider />
    <DropdownItem onclick={() => insertNextNode("Table")}>Table</DropdownItem>
  </Dropdown>
</div>
