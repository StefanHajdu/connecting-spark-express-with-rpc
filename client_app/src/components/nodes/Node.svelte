<script lang="ts">
import { Card, Dropdown, DropdownItem, DropdownDivider, Button, Tooltip, Spinner, Toggle } from "flowbite-svelte";
import { DotsHorizontalOutline, ChevronDownOutline, TrashBinOutline } from "flowbite-svelte-icons";
import { fetchSparkApi } from "$lib/clientApi";
import { tryRestoreNodes, syncOutRemovedColumns } from "$lib/utils";
import type { SparkTransformResponse } from "$lib/dtype";
import { nodeFactoryMethod, Node } from "./NodeInstance.svelte";
import LoadNode from "./LoadNode/LoadNode.svelte";
import AddColumnNode from "./AddColumn/AddColumnNode.svelte";

interface Props {
    nodesInAnalysis: Node[];
    nodeIndex: number;
    analysisId: string;
    preview(analysiId: string, nodeId: string): void;
}

let { nodesInAnalysis = $bindable(), nodeIndex, analysisId, preview }: Props = $props();

let nextNodeId = $state("");
let newNodeDropdownOpen = $state(false);
let optionsOpen = $state(false);
let summarizePromise = $state(
    Promise.resolve({
        session_id: analysisId,
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
    if (nextNodeId !== "") {
        let el = document.getElementById(nextNodeId);
        el?.scrollIntoView({ behavior: "smooth", block: "end" });
    }
});

function insertNextNode(nodeType: string) {
    let nextNode = nodeFactoryMethod(nodeType, nodesInAnalysis[nodeIndex].colsInNode);
    nodesInAnalysis = nodesInAnalysis.toSpliced(nodeIndex + 1, 0, nextNode);
    nextNodeId = nextNode.uuid;
    newNodeDropdownOpen = false;
}

async function removeNode(apiInvolved: boolean) {
    // todo: cannot remove node that is not present on backend
    if (apiInvolved) {
        let transformResponse: SparkTransformResponse = await fetchSparkApi("rpc/sessionNode/transform/removeNode", {
            session_id: analysisId,
            node_id: nodesInAnalysis[nodeIndex].uuid,
        });
        if (transformResponse) {
            syncOutRemovedColumns(nodesInAnalysis, nodeIndex);
        }
    }

    nodesInAnalysis.splice(nodeIndex, 1);
    optionsOpen = false;
}

function previewNode() {
    preview(analysisId, nodesInAnalysis[nodeIndex].uuid);
}

function summarizeNode() {
    summarizePromise = fetchSparkApi("rpc/sessionNode/action/summarize", {
        session_id: analysisId,
        node_id: nodesInAnalysis[nodeIndex].uuid,
    });
}

async function toggleNode(apiInvolved: boolean) {
    if (activeNodeStatus) {
        // enabled => disabled
        if (apiInvolved) {
            let transformResponse: SparkTransformResponse = await fetchSparkApi(
                "rpc/sessionNode/transform/removeNode",
                {
                    session_id: analysisId,
                    node_id: nodesInAnalysis[nodeIndex].uuid,
                },
            );
            if (transformResponse) {
                syncOutRemovedColumns(nodesInAnalysis, nodeIndex);
            }
        }

        nodesInAnalysis[nodeIndex].active = false;
    } else {
        // disabled => enabled
        if (apiInvolved) {
            let _ = await nodesInAnalysis[nodeIndex].submit(
                nodesInAnalysis[nodeIndex].getSubmitParams(analysisId, nodesInAnalysis, nodeIndex),
            );
        }

        nodesInAnalysis[nodeIndex].active = true;
    }
}

async function reactWhenSourceChangedWrapper(func: (apiInvolved: boolean) => Promise<void>): Promise<void> {
    const wrapped = async () => {
        if (!nodesInAnalysis[nodeIndex].invalidState.value) {
            await func(true);
        } else {
            // trigger restore on following nodes when:
            // 1. removing invalid node
            // 2. disabling invalid node
            let index = func.name === "removeNode" ? nodeIndex : nodeIndex + 1;
            await func(false);
            await tryRestoreNodes(analysisId, nodesInAnalysis, index);
        }
    };
    await wrapped();
}
</script>

<div class={"flex min-w-80 justify-center " + opacity} id={nodesInAnalysis[nodeIndex].uuid}>
    <Card class="max-w-5xl">
        <div class="flex justify-end">
            <DotsHorizontalOutline />
            <Dropdown class="w-36" bind:open={optionsOpen}>
                {#if nodesInAnalysis[nodeIndex].nodeType !== "load"}
                    <div class="flex items-stretch">
                        <DropdownItem
                            class="flex items-center"
                            disabled={!activeNodeStatus}
                            onclick={() => reactWhenSourceChangedWrapper(removeNode)}>
                            <TrashBinOutline class="mr-2" />
                            Remove
                        </DropdownItem>
                    </div>
                {/if}
            </Dropdown>
        </div>

        {#if nodesInAnalysis[nodeIndex].invalidState.value}
            <div>
                <Button id="invalid-state" outline color="red" size="xs"
                    >{nodesInAnalysis[nodeIndex].invalidState.description}</Button>
                <!-- <Tooltip arrow={false} triggeredBy="#invalid-state"
                    >{nodesInAnalysis[nodeIndex].invalidState.description}</Tooltip> -->
            </div>
        {/if}

        <div class="mb-4 mt-4 flex items-center justify-between">
            <p>id: {nodesInAnalysis[nodeIndex].uuid.slice(-5)}</p>
        </div>

        {#if nodesInAnalysis[nodeIndex].title === "Load"}<LoadNode
                bind:nodesInAnalysis={nodesInAnalysis}
                nodeIndex={nodeIndex}
                analysisId={analysisId} />
        {:else if nodesInAnalysis[nodeIndex].title === "Add Column"}<AddColumnNode
                bind:nodesInAnalysis={nodesInAnalysis}
                nodeIndex={nodeIndex}
                analysisId={analysisId}
                activeNodeStatus={activeNodeStatus} />
        {/if}

        <div class="mt-2">
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus || nodesInAnalysis[nodeIndex].invalidState.value}
                on:click={previewNode}>Preview</Button>
            <Button
                size="xs"
                color="light"
                disabled={!activeNodeStatus || nodesInAnalysis[nodeIndex].invalidState.value}
                on:click={summarizeNode}>Summarize</Button>
            {#if nodesInAnalysis[nodeIndex].title !== "Load"}
                <Toggle
                    size="small"
                    class="pt-1"
                    bind:checked={activeNodeStatus}
                    onclick={() => {
                        reactWhenSourceChangedWrapper(toggleNode);
                    }} />
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
    <Button size="xs" color="dark" disabled={!activeNodeStatus || nodesInAnalysis[nodeIndex].invalidState.value}
        >New Node<ChevronDownOutline class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
    <Dropdown bind:open={newNodeDropdownOpen}>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNextNode("Filter")}>Filter</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNextNode("Add Column")}
            >Add Column</DropdownItem>
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNextNode("Join")}>Join</DropdownItem>
        <DropdownDivider />
        <DropdownItem disabled={!activeNodeStatus} onclick={() => insertNextNode("Table")}>Table</DropdownItem>
    </Dropdown>
</div>
