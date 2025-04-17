<script lang="ts">
	import { TabItem } from 'flowbite-svelte';
	import { nodeFactoryMethod } from './nodes/NodeInstance';
	import Node from './nodes/Node.svelte';

	let { name } = $props();
	let nodesInAnalysis = $state([nodeFactoryMethod('Load')]);
	$inspect(nodesInAnalysis);
</script>

<TabItem open title={name}>
	<div id={name}>
		<p class="text-sm text-gray-500 dark:text-gray-400">
			<b>{name}</b>
		</p>
		{#each nodesInAnalysis as node}
			<Node bind:nodesInAnalysis {node} />
		{/each}
	</div>
</TabItem>
