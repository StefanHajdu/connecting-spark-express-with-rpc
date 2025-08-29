<script lang="ts">
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import type { SparkTransform } from "$lib/dtype";
import { AnalysisSession as AnalysisSessionConstructor } from "../../components/Analysis/AnalysisSessionClass.svelte";
import { analysesMock } from "$lib/analysesMock";
import type { PageProps } from "./$types";
import { nodeFactory, Node } from "../../components/Nodes/NodeClass.svelte";

let { data }: PageProps = $props();

let analyses = $state(
    analysesMock.analyses
        .filter((analysis: any) => analysis.selected)
        .map((mocked: any) => {
            return new AnalysisSessionConstructor(mocked);
        }),
);

function constructNodes(nodeTransforms: SparkTransform[]): Node[] {
    let nodes: Node[] = [];
    for (let i = 0; i < nodeTransforms.length; i++) {
        let node = nodeFactory({
            id: nodeTransforms[i].node_id,
            title: nodeTransforms[i].title,
            prevNodeId: nodeTransforms[i].prev_node_id,
            columnsOnNodeOutput: nodeTransforms[i].columns,
            active: nodeTransforms[i].active,
            invalidState: nodeTransforms[i].invalid_state,
        });
        node.setUserInput(JSON.parse(nodeTransforms[i].user_input));
        nodes.push(node);
        if (i > 0) {
            nodes[i].columnsOnNodeInput = nodes[i - 1].columnsOnNodeOutput;
        }
    }

    return nodes;
}

let aa = $state(
    data.analyses.map((analysisSnapshot: any) => {
        return new AnalysisSessionConstructor({
            ...analysisSnapshot,
            nodes: constructNodes(analysisSnapshot.nodes),
        });
    }),
);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each analyses as analysis, i (analysis.id)}
                <AnalysisSession bind:analyses={aa} analysisIndex={i} />
            {/each}
        </Tabs>
    </main>
</div>
