<script lang="ts">
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import { analyses } from "../../components/Analysis/AnalysisSessionClass.svelte";
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each analyses as analysis, i (analysis.id)}
                <AnalysisSession analysisIndex={i} />
            {/each}
        </Tabs>
    </main>
</div>
