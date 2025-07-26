<script lang="ts">
import { browser } from "$app/environment";
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import type { PageProps } from "./$types";
import type { Analysis } from "$lib/dtype";
import { rehydrateAnalysesFromRaw } from "$lib/utils";

let { data }: PageProps = $props();
let analyses = $state(browser ? rehydrateAnalysesFromRaw(data.analysesRaw) : []);

$inspect(analyses);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each analyses.filter((a: Analysis) => a.selected) as analysis}
                <AnalysisSession analysis={analysis} />
            {/each}
        </Tabs>
    </main>
</div>
