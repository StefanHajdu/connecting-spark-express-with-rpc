<script lang="ts">
import { TabItem } from "flowbite-svelte";
import { nodeFactoryMethod } from "./nodes/NodeInstance";
import Node from "./nodes/Node.svelte";

let { id, name } = $props();
let nodesInAnalysis = $state([nodeFactoryMethod("Load", [])]);
// $inspect(`nodes in analysis ${id} arr`, nodesInAnalysis);
</script>

<TabItem open title={name}>
  <div id={name}>
    <p class="text-sm text-gray-500 dark:text-gray-400">
      <b>{name}</b>
    </p>

    {#each nodesInAnalysis as node, i (node.uuid)}
      <Node bind:nodesInAnalysis={nodesInAnalysis} nodeIndex={i} analysiId={id} />
    {/each}
  </div>
</TabItem>
