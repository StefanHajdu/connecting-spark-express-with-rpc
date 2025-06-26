<script lang="ts">
import { Node } from "../NodeInstance.svelte";
import LoadDatasetForm from "./LoadDatasetForm.svelte";

interface Props {
  nodesInAnalysis: Node[];
  nodeIndex: number;
  analysisId: string;
}

let { analysisId, nodesInAnalysis = $bindable(), nodeIndex }: Props = $props();

let loaded: boolean = $state(false);
</script>

{#if loaded}
  <span class="text-m text-gray-500 dark:text-gray-400">Load Dataset</span>
{:else}
  <LoadDatasetForm
    analysisId={analysisId}
    name={"Load New Dataset"}
    bind:nodesInAnalysis={nodesInAnalysis}
    nodeIndex={nodeIndex} />
{/if}
