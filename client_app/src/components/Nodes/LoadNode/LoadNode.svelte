<script lang="ts">
import { Node, LoadNode } from "../NodeClass.svelte";
import LoadDatasetForm from "./LoadDatasetForm.svelte";
import { CsvMetadata, JsonMetadata, ParquetMetadata } from "./loadNodeTypes";

interface Props {
    nodesInAnalysis: Node[];
    nodeIndex: number;
    analysisId: string;
}

export interface LoadNodeData {
    loadSuccess: boolean;
    metadata?: CsvMetadata | JsonMetadata | ParquetMetadata;
}

let { analysisId, nodesInAnalysis = $bindable(), nodeIndex }: Props = $props();

let loadSuccess: boolean = $state(false);
</script>

{#if loadSuccess}
    {#if nodesInAnalysis[nodeIndex] instanceof LoadNode && nodesInAnalysis[nodeIndex].inputMetadata.kind == "csv"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {nodesInAnalysis[nodeIndex].inputMetadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Delimiter: {nodesInAnalysis[nodeIndex].inputMetadata.delimiter}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Include header: {nodesInAnalysis[nodeIndex].inputMetadata.include_header}</span>
    {:else if nodesInAnalysis[nodeIndex] instanceof LoadNode && nodesInAnalysis[nodeIndex].inputMetadata.kind == "json"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {nodesInAnalysis[nodeIndex].inputMetadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Multiline: {nodesInAnalysis[nodeIndex].inputMetadata.multiline}</span>
    {:else if nodesInAnalysis[nodeIndex] instanceof LoadNode && nodesInAnalysis[nodeIndex].inputMetadata.kind == "parquet"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {nodesInAnalysis[nodeIndex].inputMetadata.path}</span>
    {/if}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Replace Dataset"}
        color={"dark"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadSuccess={loadSuccess}
        nodeIndex={nodeIndex} />
{:else}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Load New Dataset"}
        color={"blue"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadSuccess={loadSuccess}
        nodeIndex={nodeIndex} />
{/if}
