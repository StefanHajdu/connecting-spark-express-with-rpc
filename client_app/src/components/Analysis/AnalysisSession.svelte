<script lang="ts">
import { TabItem } from "flowbite-svelte";
import PreviewFooter from "../PreviewFooter.svelte";
import Node from "../Nodes/Node.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

interface Props {
    analysisIndex: number;
}

let { analysisIndex }: Props = $props();
let previewFooter: any;

async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
    await previewFooter.forwardPreview(analysiId, nodeId);
}
</script>

<TabItem open title={globalAnalysesState.analyses[analysisIndex].name}>
    <main class="bg-white-500 space-y-4 p-4">
        <div id={globalAnalysesState.analyses[analysisIndex].name}>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                <b>{globalAnalysesState.analyses[analysisIndex].name}</b>
            </p>

            {#each globalAnalysesState.analyses[analysisIndex].nodes as node, i (node.id)}
                <Node
                    analysisIndex={analysisIndex}
                    nodeIndex={i}
                    preview={(analysisId, nodeId) => {
                        forwardPreview(analysisId, nodeId);
                    }} />
            {/each}
        </div>
    </main>
    <PreviewFooter bind:this={previewFooter} />
</TabItem>
