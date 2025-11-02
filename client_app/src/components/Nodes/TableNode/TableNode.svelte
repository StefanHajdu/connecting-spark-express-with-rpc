<script lang="ts">
import { Spinner } from "flowbite-svelte";
import { globalAnalysesState } from "../../Analysis/AnalysisSessionClass.svelte";
import { Preview } from "../../PreviewStore.svelte";
import DataFrameTable from "../../DataFrameTable.svelte";

interface Props {
  analysisIndex: number;
  nodeIndex: number;
}

let { analysisIndex, nodeIndex }: Props = $props();

let node = $derived(globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex]);
let tablePreview = $state(new Preview());

let previewPromise = $derived.by(async () => {
  if (!node.prevNodeId) {
    throw new Error("No previous node to display");
  }

  await tablePreview.run(globalAnalysesState.analyses[analysisIndex].session_id, node.prevNodeId, 1000);

  return tablePreview;
});
</script>

<div class="mb-2">
  <p class="text-sm font-semibold text-gray-700">Table View</p>
  <p class="text-xs text-gray-500">Displaying data from the previous node</p>
</div>

{#await previewPromise}
  <div class="flex justify-center items-center py-8">
    <Spinner size={8} />
    <p class="ml-2">Loading table...</p>
  </div>
{:then preview}
  {#if preview.data.length > 0}
    <div class="mt-4 flex flex-col items-center w-full">
      <div class="mb-2 flex gap-2">
        <p class="font-normal text-xs">{preview.data.length} rows,</p>
        <p class="font-semibold text-xs">{preview.columns.length} columns</p>
      </div>
      <div class="max-h-96 max-w-full overflow-auto border rounded">
        <DataFrameTable previewObject={preview} />
      </div>
    </div>
  {:else}
    <div class="py-4 text-gray-500">
      <p>No data to display</p>
    </div>
  {/if}
{:catch error}
  <div class="text-red-500 py-4">
    <p>Error: {error.message}</p>
  </div>
{/await}
