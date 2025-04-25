<script lang="ts">
import {
  Card,
  Dropdown,
  DropdownItem,
  DropdownDivider,
  Button,
  Spinner,
} from "flowbite-svelte";
import {
  DotsHorizontalOutline,
  ChevronDownOutline,
} from "flowbite-svelte-icons";
import { fetchSparkApi } from "$lib/clientApi";
import { actionState, requestAction } from "$lib/actionState.svelte";
import { nodeFactoryMethod } from "./NodeInstance";
import LoadNode from "./LoadNode.svelte";

let {
  nodesInAnalysis = $bindable(),
  node,
  analysiId,
  analysisRandomSeed,
} = $props();
let dataFrameColumns = $state([{ name: "", dtype: "" }]);
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

function getNodeIdx(uuid: string): number {
  return nodesInAnalysis.findIndex((node: any) => node.uuid === uuid);
}

function insertNextNode(nodeType: string) {
  let nodeIdx = getNodeIdx(node.uuid);
  let nextNode = nodeFactoryMethod(nodeType);
  nodesInAnalysis = nodesInAnalysis.toSpliced(nodeIdx + 1, 0, nextNode);
  nextNodeId = nextNode.uuid;
  dropdownOpen = false;
}

function removeNode() {
  let itemIdx = nodesInAnalysis.findIndex((n: any) => n.uuid === node.uuid);
  nodesInAnalysis.splice(itemIdx, 1);
}

function previewEvent() {
  requestAction(analysiId, analysisRandomSeed, dataFrameColumns, node.uuid);
}

function summarizeEvent() {
  if (!actionState.inProgress) {
    summarizePromise = fetchSparkApi("summarize", {
      session_id: analysiId,
      node_id: node.uuid,
    });
  } else {
    console.log("summarize, rejected");
  }
}

$inspect("node", actionState);
</script>

<div class="flex min-w-80 justify-center" id={node.uuid}>
  <Card size="lg" padding="md">
    <div class="flex justify-end">
      <DotsHorizontalOutline />
      <Dropdown class="w-36">
        {#if node.nodeType !== "load"}
          <DropdownItem onclick={removeNode}>Remove</DropdownItem>
        {/if}
      </Dropdown>
    </div>
    <div class="mb-4 flex items-center justify-between">
      <p>id: {node.uuid.slice(-5)}</p>
      <p>type: {node.nodeType}</p>
    </div>
    {#if node.title === "Load"}<LoadNode
        bind:dataFrameColumns={dataFrameColumns}
        node={node}
        analysiId={analysiId} />{/if}
    <div class="mt-2">
      <Button size="xs" color="light" on:click={previewEvent}>Preview</Button>
      <Button size="xs" color="light" on:click={summarizeEvent}
        >Summarize</Button>
    </div>
    {#await summarizePromise}
      <Spinner size={6} />
    {:then summarizeResponse}
      {#if summarizeResponse.count > 0}
        <p>{summarizeResponse.count}</p>
      {/if}
    {/await}
  </Card>
</div>
<div class="flex justify-center">
  <Button size="xs" color="dark"
    >Dropdown button<ChevronDownOutline
      class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
  <Dropdown bind:open={dropdownOpen}>
    <DropdownItem onclick={() => insertNextNode("Filter")}>Filter</DropdownItem>
    <DropdownItem onclick={() => insertNextNode("Add Column")}
      >Add Column</DropdownItem>
    <DropdownItem onclick={() => insertNextNode("Join")}>Join</DropdownItem>
    <DropdownDivider />
    <DropdownItem onclick={() => insertNextNode("Table")}>Table</DropdownItem>
  </Dropdown>
</div>
