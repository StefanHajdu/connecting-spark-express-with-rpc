<script lang="ts">
import { AnalysisSession, saveAnalysesToLocalStorage } from "../../Analysis/AnalysisSessionClass.svelte";
import { LoadNode } from "../NodeClass.svelte";
import LoadDatasetForm from "./LoadDatasetForm.svelte";

interface Props {
    analyses: AnalysisSession[];
    analysisIndex: number;
    nodeIndex: number;
}
let { analyses = $bindable(), analysisIndex, nodeIndex }: Props = $props();

// $effect(() => {
//     if (analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode) {
//         // hit UI dynamic instance proprety to trigger effect
//         analyses[analysisIndex].nodes[nodeIndex].userInput;
//         // console.log("load node is reacting id:", analyses[analysisIndex].nodes[nodeIndex].userInput);
//         saveAnalysesToLocalStorage(analyses);
//     }
// });
</script>

{#if analyses[analysisIndex].nodes[nodeIndex].submitted}
    {#if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].userInput.kind == "csv"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].userInput.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Delimiter: {analyses[analysisIndex].nodes[nodeIndex].userInput.delimiter}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Include header: {analyses[analysisIndex].nodes[nodeIndex].userInput.include_header}</span>
    {:else if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].userInput.kind == "json"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].userInput.path}</span>
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Multiline: {analyses[analysisIndex].nodes[nodeIndex].userInput.multiline}</span>
    {:else if analyses[analysisIndex].nodes[nodeIndex] instanceof LoadNode && analyses[analysisIndex].nodes[nodeIndex].userInput.kind == "parquet"}
        <span class="text-m text-gray-500 dark:text-gray-400"
            >Path: {analyses[analysisIndex].nodes[nodeIndex].userInput.path}</span>
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
