<script lang="ts">
import { browser } from "$app/environment";
import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/AnalysisSession.svelte";
import { Tabs } from "flowbite-svelte";
import { LS_KEY_ANALYSES, fromLocalStorage } from "../../lib/localStorageHandles";
import type { Analysis } from "$lib/dtype";

let analyses = $state(browser ? fromLocalStorage(LS_KEY_ANALYSES) : []);
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
