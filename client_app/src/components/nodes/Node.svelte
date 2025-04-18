<script lang="ts">
import {
  Card,
  Dropdown,
  DropdownItem,
  DropdownDivider,
  Button,
} from "flowbite-svelte";
import {
  DotsHorizontalOutline,
  ChevronDownOutline,
} from "flowbite-svelte-icons";
import { nodeFactoryMethod } from "./NodeInstance";
import { type SparkActionlResponse, fetchSparkApi } from "$lib/clientApi";
import LoadNode from "./LoadNode.svelte";

let { nodesInAnalysis = $bindable(), node, analysis_id } = $props();
let dataFrameColumns = $state([{ name: "", dtype: "" }]);
let nextNodeId = $state("");
let dropdownOpen = $state(false);
let summarizeState = $state({
  session_id: analysis_id,
  msg: "",
  columns: "",
  schema: "",
  count: -1,
});

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

async function preview() {}

async function summarize() {
  let countResponse: SparkActionlResponse = await fetchSparkApi("summarize", {
    session_id: analysis_id,
    node_id: node.uuid,
  });

  if (countResponse) {
    summarizeState = { ...countResponse };
  }
}

$inspect(dataFrameColumns);
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
        analysis_id={analysis_id} />{/if}
    <div class="mt-2">
      <Button size="xs" color="light" on:click={preview}>Preview</Button>
      <Button size="xs" color="light" on:click={summarize}>Summarize</Button>
      {#if summarizeState.count > -1}
        <p>{summarizeState.count}</p>
      {/if}
    </div>
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
