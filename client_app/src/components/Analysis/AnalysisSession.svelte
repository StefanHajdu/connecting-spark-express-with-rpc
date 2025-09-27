<script lang="ts">
import { TabItem } from "flowbite-svelte";
import Node from "../Nodes/Node.svelte";
import { footerPreview } from "../PreviewStore.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

interface Props {
  analysisIndex: number;
}

let { analysisIndex }: Props = $props();
async function forwardPreview(analysisId: string, nodeId: string): Promise<void> {
  footerPreview.visibilityToggle(true);
  await footerPreview.run(analysisId, nodeId);
}
</script>

<TabItem open title={globalAnalysesState.analyses[analysisIndex].name}>
  <div id={globalAnalysesState.analyses[analysisIndex].name} class="overflow-y">
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
</TabItem>
