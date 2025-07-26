<script lang="ts">
import type { Analysis } from "$lib/dtype";
import { LoadNode } from "../NodeClass.svelte";
import LoadDatasetForm from "./LoadDatasetForm.svelte";

interface Props {
    analyses: Analysis[];
    analysisIndex: number;
    nodeIndex: number;
}
let { analyses = $bindable(), analysisIndex, nodeIndex }: Props = $props();
</script>

{#if analyses[analysisIndex].nodes[nodeIndex].submitted}
    {#if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].inputMetadata.kind == "csv"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Delimiter: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.delimiter}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Include header: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.include_header}</span>
    {:else if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].inputMetadata.kind == "json"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Multiline: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.multiline}</span>
    {:else if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].inputMetadata.kind == "parquet"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].inputMetadata.path}</span>
    {/if}
    <LoadDatasetForm
        name={"Replace Dataset"}
        color={"dark"}
        bind:analyses={analyses}
        analysisIndex={analysisIndex}
        nodeIndex={nodeIndex} />
{:else}
    <LoadDatasetForm
        name={"Load New Dataset"}
        color={"dark"}
        bind:analyses={analyses}
        analysisIndex={analysisIndex}
        nodeIndex={nodeIndex} />
{/if}
