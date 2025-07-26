<script lang="ts">
import Header from "../components/Header.svelte";
import Footer from "../components/Footer.svelte";
import NewAnalysisForm from "../components/Analysis/NewAnalysisForm.svelte";
import AnalysisTable from "../components/Analysis/AnalysisTable.svelte";
import { analysesMock } from "$lib/analysesMock";
import { AnalysisC } from "../components/Analysis/AnalysisClass.svelte";

let analyses = analysesMock.analyses.map((mocked: any) => {
    return new AnalysisC(mocked);
});
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
    <Header />

    <main class="bg-white-500 space-y-4 p-4">
        <div>
            <NewAnalysisForm bind:analyses={analyses} />
        </div>
        <div>
            <AnalysisTable bind:analyses={analyses} />
        </div>
    </main>

    <Footer />
</div>
