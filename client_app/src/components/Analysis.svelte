<script lang="ts">
import { TabItem } from "flowbite-svelte";
import { nodeFactoryMethod } from "./nodes/NodeInstance";
import Node from "./nodes/Node.svelte";

let { id, name } = $props();
let nodesInAnalysis = $state([nodeFactoryMethod("Load")]);
let randomSeed = $derived.by(() => {
  return Math.random() * nodesInAnalysis.length;
});
$inspect(nodesInAnalysis, randomSeed);
</script>

<TabItem open title={name}>
  <div id={name}>
    <p class="text-sm text-gray-500 dark:text-gray-400">
      <b>{name}</b>
    </p>
    {#each nodesInAnalysis as node}
      <Node
        bind:nodesInAnalysis={nodesInAnalysis}
        node={node}
        analysiId={id}
        analysisRandomSeed={randomSeed} />
    {/each}
  </div>
</TabItem>
