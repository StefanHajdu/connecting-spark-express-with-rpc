<script lang="ts">
import { Card, Dropdown, DropdownItem, DropdownDivider, Button, Spinner, Toggle } from "flowbite-svelte";
import { DotsHorizontalOutline, ChevronDownOutline, TrashBinOutline } from "flowbite-svelte-icons";
import { fetchSparkApi } from "$lib/clientApi";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";
import LoadNode from "./LoadNode/LoadNode.svelte";
import AddColumnNode from "./AddColumn/AddColumnNode.svelte";

interface Props {
    analysisIndex: number;
    nodeIndex: number;
    preview(analysiId: string, nodeId: string): void;
}

let { analysisIndex, nodeIndex, preview }: Props = $props();

let nodeIdDOM = $state("");
let newNodeDropdownOpen = $state(false);
let optionsOpen = $state(false);
let summarizePromise = $state(
    Promise.resolve({
        session_id: globalAnalysesState.analyses[analysisIndex].id,
        msg: "",
        columns: "",
        schema: "",
        count: -1,
    }),
);
let activeNodeStatus = $state(globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].active);
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
    let node = globalAnalysesState.analyses[analysisIndex].createNode(title, nodeIndex);
    await globalAnalysesState.analyses[analysisIndex].insertNode(node, nodeIndex);

    nodeIdDOM = node.id;
    newNodeDropdownOpen = false;
}

async function removeNode() {
    await globalAnalysesState.analyses[analysisIndex].removeNode(nodeIndex);

    optionsOpen = false;
}

async function toggleNode() {
    await globalAnalysesState.analyses[analysisIndex].toggleNode(nodeIndex, !activeNodeStatus);
}

function previewNode() {
    preview(
        globalAnalysesState.analyses[analysisIndex].id,
        globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].id,
    );
}

function summarizeNode() {
    summarizePromise = fetchSparkApi("rpc/sessionNode/action/summarize", {
        session_id: globalAnalysesState.analyses[analysisIndex].id,
        node_id: globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].id,
    });
}
</script>

<div
    class={"flex min-w-80 justify-center " + opacity}
    id={globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].id}>
    <Card class="max-w-5xl">
        <div class="flex justify-end">
            <DotsHorizontalOutline />
            <Dropdown class="w-36" bind:open={optionsOpen}>
                {#if globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].nodeType !== "input"}
                    <div class="flex items-stretch">
                        <DropdownItem class="flex items-center" disabled={!activeNodeStatus} onclick={removeNode}>
                            <TrashBinOutline class="mr-2" />
                            Remove
                        </DropdownItem>
                    </div>
                {/if}
            </Dropdown>
        </div>

        {#if globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
            <div>
                <Button id="invalid-state" outline color="red" size="xs"
                    >{globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].invalidState.error_msg}</Button>
            </div>
        {/if}

        <div class="mb-4 mt-4 flex items-center justify-between">
            <p>id: {globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].id.slice(-5)}</p>
            <p>
                prev_id: {globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].prevNodeId
                    ? globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].prevNodeId.slice(-5)
                    : "no prev id"}
            </p>
        </div>

        {#if globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].title === "LoadNode"}<LoadNode
                analysisIndex={analysisIndex}
                nodeIndex={nodeIndex} />
        {:else if globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].title === "AddColumnNode"}<AddColumnNode
                analysisIndex={analysisIndex}
                nodeIndex={nodeIndex} />
        {/if}

        <div class="mt-2">
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus ||
                    globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
                on:click={previewNode}>Preview</Button>
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus ||
                    globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
                on:click={summarizeNode}>Summarize</Button>
            {#if globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].title !== "LoadNode"}
                <div>
                    <Toggle size="small" class="pt-1" bind:checked={activeNodeStatus} onclick={toggleNode} />
                </div>
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
        disabled={!activeNodeStatus || globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].invalidState.active}
        >New Node<ChevronDownOutline class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
    <Dropdown bind:open={newNodeDropdownOpen}>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("FilterNode")}>Filter</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("AddColumnNode")}>Add Column</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("JoinNode")}>Join</DropdownItem>
        <DropdownDivider />
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNode("TableNode")}>Table</DropdownItem>
    </Dropdown>
</div>
