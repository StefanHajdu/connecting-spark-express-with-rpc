<script lang="ts">
import { TabItem } from "flowbite-svelte";
import PreviewFooter from "../PreviewFooter.svelte";
import Node from "../Nodes/Node.svelte";
import { AnalysisSession } from "./AnalysisSessionClass.svelte";

interface Props {
    analyses: AnalysisSession[];
    analysisIndex: number;
}

let { analyses = $bindable(), analysisIndex }: Props = $props();
let previewFooterComponent: any;

async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
    await previewFooterComponent.forwardPreview(analysiId, nodeId);
}
</script>

<TabItem open title={analyses[analysisIndex].name}>
    <main class="bg-white-500 space-y-4 p-4">
        <div id={analyses[analysisIndex].name}>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                <b>{analyses[analysisIndex].name}</b>
            </p>

            {#each analyses[analysisIndex].nodes as node, i (node.id)}
                <Node
                    bind:analyses={analyses}
                    analysisIndex={analysisIndex}
                    nodeIndex={i}
                    preview={(analysisId, nodeId) => {
                        forwardPreview(analysisId, nodeId);
                    }} />
            {/each}
        </div>
    </main>
    <PreviewFooter bind:this={previewFooterComponent} />
</TabItem>
