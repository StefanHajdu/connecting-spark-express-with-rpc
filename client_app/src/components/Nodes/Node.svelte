<script lang="ts">
import { Card, Dropdown, DropdownItem, DropdownDivider, Button, Spinner, Toggle } from "flowbite-svelte";
import { DotsHorizontalOutline, ChevronDownOutline, TrashBinOutline } from "flowbite-svelte-icons";
import { fetchSparkApi } from "$lib/clientApi";
import { AnalysisSession } from "../Analysis/AnalysisSessionClass.svelte";
import LoadNode from "./LoadNode/LoadNode.svelte";
import AddColumnNode from "./AddColumn/AddColumnNode.svelte";

interface Props {
    analyses: AnalysisSession[];
    analysisIndex: number;
    nodeIndex: number;
    preview(analysiId: string, nodeId: string): void;
}

let { analyses = $bindable(), analysisIndex, nodeIndex, preview }: Props = $props();

let nodeIdDOM = $state("");
let newNodeDropdownOpen = $state(false);
let optionsOpen = $state(false);
let summarizePromise = $state(
    Promise.resolve({
        session_id: analyses[analysisIndex].id,
        msg: "",
        columns: "",
        schema: "",
        count: -1,
    }),
);
let activeNodeStatus = $state(true);
let opacity = $derived.by(() => {
    return activeNodeStatus ? "opacity-100" : "opacity-40";
});

$effect(() => {
    if (nodeIdDOM !== "") {
        let el = document.getElementById(nodeIdDOM);
        el?.scrollIntoView({ behavior: "smooth", block: "end" });
    }
});

async function insertNode(title: string) {
    let node = analyses[analysisIndex].createNode(title, nodeIndex);
    await analyses[analysisIndex].insertNode(node, nodeIndex);

    nodeIdDOM = node.id;
    newNodeDropdownOpen = false;
}

async function removeNode() {
    await analyses[analysisIndex].removeNode(nodeIndex);

    optionsOpen = false;
}

async function toggleNode() {
    await analyses[analysisIndex].toggleNode(nodeIndex, !activeNodeStatus);
}

function previewNode() {
    preview(analyses[analysisIndex].id, analyses[analysisIndex].nodes[nodeIndex].id);
}

function summarizeNode() {
    summarizePromise = fetchSparkApi("rpc/sessionNode/action/summarize", {
        session_id: analyses[analysisIndex].id,
        node_id: analyses[analysisIndex].nodes[nodeIndex].id,
    });
}
</script>

<div class={"flex min-w-80 justify-center " + opacity} id={analyses[analysisIndex].nodes[nodeIndex].id}>
    <Card class="max-w-5xl">
        <div class="flex justify-end">
            <DotsHorizontalOutline />
            <Dropdown class="w-36" bind:open={optionsOpen}>
                {#if analyses[analysisIndex].nodes[nodeIndex].nodeType !== "input"}
                    <div class="flex items-stretch">
                        <DropdownItem class="flex items-center" disabled={!activeNodeStatus} onclick={removeNode}>
                            <TrashBinOutline class="mr-2" />
                            Remove
                        </DropdownItem>
                    </div>
                {/if}
            </Dropdown>
        </div>

        {#if analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
            <div>
                <Button id="invalid-state" outline color="red" size="xs"
                    >{analyses[analysisIndex].nodes[nodeIndex].invalidState.error_msg}</Button>
            </div>
        {/if}

        <div class="mb-4 mt-4 flex items-center justify-between">
            <p>id: {analyses[analysisIndex].nodes[nodeIndex].id.slice(-5)}</p>
            <p>
                prev_id: {analyses[analysisIndex].nodes[nodeIndex].prevNodeId
                    ? analyses[analysisIndex].nodes[nodeIndex].prevNodeId.slice(-5)
                    : "no prev id"}
            </p>
        </div>

        {#if analyses[analysisIndex].nodes[nodeIndex].title === "LoadNode"}<LoadNode
                bind:analyses={analyses}
                analysisIndex={analysisIndex}
                nodeIndex={nodeIndex} />
        {:else if analyses[analysisIndex].nodes[nodeIndex].title === "AddColumnNode"}<AddColumnNode
                bind:analyses={analyses}
                analysisIndex={analysisIndex}
                nodeIndex={nodeIndex} />
        {/if}

        <div class="mt-2">
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus || analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
                on:click={previewNode}>Preview</Button>
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus || analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
                on:click={summarizeNode}>Summarize</Button>
            {#if analyses[analysisIndex].nodes[nodeIndex].title !== "LoadNode"}
                <Toggle size="small" class="pt-1" bind:checked={activeNodeStatus} onclick={toggleNode} />
            {/if}
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
    <Button
        size="xs"
        color="dark"
        disabled={!activeNodeStatus || analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
        >New Node<ChevronDownOutline class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
    <Dropdown bind:open={newNodeDropdownOpen}>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("FilterNode")}>Filter</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("AddColumnNode")}>Add Column</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("JoinNode")}>Join</DropdownItem>
        <DropdownDivider />
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("TableNode")}>Table</DropdownItem>
    </Dropdown>
</div>
