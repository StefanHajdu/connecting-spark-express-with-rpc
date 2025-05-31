<script lang="ts">
import { TabItem } from "flowbite-svelte";
import PreviewFooter from "./PreviewFooter.svelte";
import { nodeFactoryMethod } from "./nodes/NodeInstance.svelte";
import Node from "./nodes/Node.svelte";

let { id, name } = $props();
let nodesInAnalysis = $state([nodeFactoryMethod("Load", [])]);
let previewFooterComponent: any;

async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
  await previewFooterComponent.forwardPreview(analysiId, nodeId);
}

// $inspect(`nodes in analysis ${id} arr`, nodesInAnalysis);
</script>

<TabItem open title={name}>
  <main class="bg-white-500 space-y-4 p-4">
    <div id={name}>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        <b>{name}</b>
      </p>

      {#each nodesInAnalysis as node, i (node.uuid)}
        <Node
          bind:nodesInAnalysis={nodesInAnalysis}
          nodeIndex={i}
          analysisId={id}
          preview={(analysisId, nodeId) => {
            forwardPreview(analysisId, nodeId);
          }} />
      {/each}
    </div>
  </main>
  <PreviewFooter bind:this={previewFooterComponent} />
</TabItem>
