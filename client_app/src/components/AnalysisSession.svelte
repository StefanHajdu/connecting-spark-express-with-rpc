<script lang="ts">
import { TabItem } from "flowbite-svelte";
import PreviewFooter from "./PreviewFooter.svelte";
import { nodeFactoryMethod } from "./nodes/NodeInstance.svelte";
import Node from "./nodes/Node.svelte";
import type { Analysis } from "$lib/dtype";

interface Props {
    analysis: Analysis;
}

let { analysis }: Props = $props();
let previewFooterComponent: any;

async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
    await previewFooterComponent.forwardPreview(analysiId, nodeId);
}
</script>

<TabItem open title={analysis.name}>
    <main class="bg-white-500 space-y-4 p-4">
        <div id={analysis.name}>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                <b>{analysis.name}</b>
            </p>

            {#each analysis.nodes as node, i (node.uuid)}
                <Node
                    analysis={analysis}
                    nodeIndex={i}
                    preview={(analysisId, nodeId) => {
                        forwardPreview(analysisId, nodeId);
                    }} />
            {/each}
        </div>
    </main>
    <PreviewFooter bind:this={previewFooterComponent} />
</TabItem>
