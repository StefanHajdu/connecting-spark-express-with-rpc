<script lang="ts">
import { browser } from "$app/environment";
import Header from "../../components/Header.svelte";
import Analysis from "../../components/Analysis.svelte";
import { Tabs } from "flowbite-svelte";
import { STORAGE_KEY_SELECTED_ANALYSES, STORAGE_KEY_ANALYSES, fromLocalStorage } from "../../lib/localStorageHandles";

const scopedAnalyses = loadScoped();

function loadScoped(): any[] {
    if (browser) {
        let analyses = fromLocalStorage(STORAGE_KEY_ANALYSES);
        let scopedKeys = fromLocalStorage(STORAGE_KEY_SELECTED_ANALYSES);
        return scopedKeys.map((key: string) => {
            return analyses[key];
        });
    }
    return [];
}

$inspect("analyses arr", scopedAnalyses);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <Tabs>
            {#each scopedAnalyses as analysis}
                <Analysis name={analysis.name} id={analysis.id} />
            {/each}
        </Tabs>
    </main>
</div>
