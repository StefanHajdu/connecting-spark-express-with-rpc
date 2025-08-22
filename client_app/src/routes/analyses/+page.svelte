<script lang="ts">
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import { AnalysisSession as AnalysisSessionConstructor } from "../../components/Analysis/AnalysisSessionClass.svelte";
import { analysesMock } from "$lib/analysesMock";

let analyses = $state(
    analysesMock.analyses
        .filter((analysis: any) => analysis.selected)
        .map((mocked: any) => {
            return new AnalysisSessionConstructor(mocked);
        }),
);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each analyses as analysis, i (analysis.id)}
                <AnalysisSession bind:analyses={analyses} analysisIndex={i} />
            {/each}
        </Tabs>
    </main>
</div>
