<script lang="ts">
import { TabItem, CloseButton } from "flowbite-svelte";
import { Pane, Splitpanes } from "svelte-splitpanes";
import PreviewFooter from "../PreviewFooter.svelte";
import Node from "../Nodes/Node.svelte";
import DataFrameTable from "../DataFrameTable.svelte";
import { footerPreview } from "../PreviewStore.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

interface Props {
  analysisIndex: number;
}

let { analysisIndex }: Props = $props();
let previewFooter: any;
let rerenderState = $derived.by(() => {
  return footerPreview.salt;
});

let paneVisible = $derived.by(() => {
  return footerPreview.visible;
});
let resize = $state(0);

async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
  await previewFooter.preview(analysiId, nodeId);
}

function handleMessage(event: any) {
  resize = Math.round(event.detail[1].size);
}

$inspect(resize);
</script>

<TabItem open title={globalAnalysesState.analyses[analysisIndex].name}>
  <Splitpanes class="default-theme" horizontal={true} on:resize={handleMessage}>
    <Pane size={20}>
      <div id={globalAnalysesState.analyses[analysisIndex].name} class="overflow-y">
        <p class="text-sm text-gray-500 dark:text-gray-400">
          <b>{globalAnalysesState.analyses[analysisIndex].name}</b>
        </p>

        <Node
          analysisIndex={analysisIndex}
          nodeIndex={0}
          preview={(analysisId, nodeId) => {
            forwardPreview(analysisId, nodeId);
          }} />
        {#each globalAnalysesState.analyses[analysisIndex].nodes.slice(1) as node, i (node.id)}
          <Node
            analysisIndex={analysisIndex}
            nodeIndex={i + 1}
            preview={(analysisId, nodeId) => {
              forwardPreview(analysisId, nodeId);
            }} />
        {/each}
      </div>
    </Pane>
    <Pane snapSize={5} size={40}>
      {#if paneVisible}
        <div class="mt-2 mb-2 flex h-6 items-center">
          <div class="mb-2">
            <p>Preview</p>
            <div class="flex justify-normal">
              <p class="font-normal text-xs">{footerPreview.data.length} rows,</p>
              <p class="ml-1 font-semibold text-xs">{footerPreview.columns.length} columns</p>
            </div>
          </div>

          <CloseButton
            on:click={() => {
              footerPreview.visibilityToggle(false);
            }}
            class="dark:text-white" />
        </div>
        {#key rerenderState}
          <DataFrameTable previewObject={footerPreview} heightCss={`h-${80}`} />
        {/key}
      {/if}
    </Pane>
  </Splitpanes>
  <PreviewFooter bind:this={previewFooter} />
</TabItem>
