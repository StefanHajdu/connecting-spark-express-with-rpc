<script lang="ts">
import { browser } from "$app/environment";
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import type { PageProps } from "./$types";
import { rehydrateAnalysesFromRaw } from "$lib/utils";

let { data }: PageProps = $props();
let analyses = $state(browser ? rehydrateAnalysesFromRaw(data.analysesRaw) : []);

$inspect("from /analyses load", analyses);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each analyses.filter((analysis) => analysis.selected) as analysis, i (analysis.id)}
                <AnalysisSession bind:analyses={analyses} analysisIndex={i} />
            {/each}
        </Tabs>
    </main>
</div>
