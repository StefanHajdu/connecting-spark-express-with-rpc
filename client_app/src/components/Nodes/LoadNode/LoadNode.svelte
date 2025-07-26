<script lang="ts">
import { Node } from "../NodeClass.svelte";
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

let loadNodeData: LoadNodeData = $state({ loadSuccess: false });
</script>

{#if loadNodeData.loadSuccess}
    {#if loadNodeData.metadata instanceof CsvMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadNodeData.metadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400">Delimiter: {loadNodeData.metadata.delimiter}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Include header: {loadNodeData.metadata.includeHeader}</span>
    {:else if loadNodeData.metadata instanceof JsonMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadNodeData.metadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400">Multiline: {loadNodeData.metadata.multiline}</span>
    {:else if loadNodeData.metadata instanceof ParquetMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadNodeData.metadata.path}</span>
    {/if}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Replace Dataset"}
        color={"dark"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadNodeData={loadNodeData}
        nodeIndex={nodeIndex} />
{:else}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Load New Dataset"}
        color={"blue"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadNodeData={loadNodeData}
        nodeIndex={nodeIndex} />
{/if}
