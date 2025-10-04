<script lang="ts">
import { TabItem } from "flowbite-svelte";
import Node from "../Nodes/Node.svelte";
import { footerPreview } from "../PreviewStore.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";
import { Pane, Splitpanes } from "svelte-splitpanes";

interface Props {
  analysisIndex: number;
}

let { analysisIndex }: Props = $props();

async function forwardPreview(analysisId: string, nodeId: string): Promise<void> {
  footerPreview.visibilityToggle(true);
  await footerPreview.run(analysisId, nodeId);
}

let previewPaneSize = $state(0);
let previewVisible = $derived.by(() => {
  return footerPreview.visible;
});

function handleResize(event: any) {
  previewPaneSize = Math.round(event.detail[1].size);
  footerPreview.visible = previewPaneSize > 0;
}
</script>

<TabItem open divClass="h-full" title={globalAnalysesState.analyses[analysisIndex].name}>
  <div id={globalAnalysesState.analyses[analysisIndex].name} class="flex flex-col overflow-hidden h-full">
    <Splitpanes horizontal={true} style="height: full" on:resize={handleResize}>
      <Pane minSize={30} maxSize={100}>
        <div class="overflow-y-auto max-h-full">
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
      <Pane snapSize={5} size={previewVisible ? 50 : 0}>
        <div class="m-2">
          <p>Preview</p>
          <div class="flex justify-normal">
            <p class="font-normal text-xs">{footerPreview.data.length} rows,</p>
            <p class="ml-1 font-semibold text-xs">{footerPreview.columns.length} columns</p>
          </div>
        </div>
      </Pane>
    </Splitpanes>
  </div>
</TabItem>
