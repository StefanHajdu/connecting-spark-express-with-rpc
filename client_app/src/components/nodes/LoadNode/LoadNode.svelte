<script lang="ts">
import { Node } from "../NodeInstance.svelte";
import LoadDatasetForm from "./LoadDatasetForm.svelte";
import { type LoadedDataset, CsvMetadata, JsonMetadata, ParquetMetadata } from "./loadTypes";

interface Props {
    nodesInAnalysis: Node[];
    nodeIndex: number;
    analysisId: string;
}

let { analysisId, nodesInAnalysis = $bindable(), nodeIndex }: Props = $props();

let loadedDataset: LoadedDataset | { loadSuccess: false } = $state({ loadSuccess: false });
</script>

{#if loadedDataset.loadSuccess}
    {#if loadedDataset.metadata instanceof CsvMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadedDataset.metadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400">Delimiter: {loadedDataset.metadata.delimiter}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Inlcude header{loadedDataset.metadata.includeHeader}</span>
    {:else if loadedDataset.metadata instanceof JsonMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadedDataset.metadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400">Multiline: {loadedDataset.metadata.multiline}</span>
    {:else if loadedDataset.metadata instanceof ParquetMetadata}
        <span class="text-m text-gray-500 dark:text-gray-400">Path: {loadedDataset.metadata.path}</span>
    {/if}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Replace Dataset"}
        color={"dark"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadedDataset={loadedDataset}
        nodeIndex={nodeIndex} />
{:else}
    <LoadDatasetForm
        analysisId={analysisId}
        name={"Load New Dataset"}
        color={"blue"}
        bind:nodesInAnalysis={nodesInAnalysis}
        bind:loadedDataset={loadedDataset}
        nodeIndex={nodeIndex} />
{/if}
