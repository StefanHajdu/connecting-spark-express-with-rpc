<script lang="ts">
import Header from "../components/Header.svelte";
import Footer from "../components/Footer.svelte";
import NewAnalysisForm from "../components/NewAnalysisForm.svelte";
import AnalysisTable from "../components/AnalysisTable.svelte";
import type { PageProps } from "./$types";
import type { Analysis } from "$lib/dtype";
import { STORAGE_KEY_ANALYSES, toLocalStorage } from "$lib/localStorageHandles";

let { data }: PageProps = $props();

let analyses: Analysis[] = $state(data.analyses);

$effect(() => {
    toLocalStorage(STORAGE_KEY_ANALYSES, { analyses: analyses });
});

$inspect(analyses);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <div>
            <NewAnalysisForm analyses={analyses} />
        </div>
        <div>
            <AnalysisTable bind:analyses={analyses} />
        </div>
    </main>

    <Footer />
</div>
