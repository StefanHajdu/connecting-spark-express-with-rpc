<script lang="ts">
import Header from "../components/Header.svelte";
import Footer from "../components/Footer.svelte";
import NewAnalysisForm from "../components/Analysis/NewAnalysisForm.svelte";
import AnalysisTable from "../components/Analysis/AnalysisTable.svelte";
import { analysesMock } from "$lib/analysesMock";
import { AnalysisSession } from "../components/Analysis/AnalysisSessionClass.svelte";

let persistedAnalyses = $state(
  analysesMock.analyses.map((mocked: any) => {
    return new AnalysisSession(mocked);
  }),
);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
  <Header />

  <main class="bg-white-500 space-y-4 p-4">
    <div>
      <NewAnalysisForm />
    </div>
    <!-- <div>
            <AnalysisTable bind:persistedAnalyses={persistedAnalyses} />
        </div> -->
  </main>

  <Footer />
</div>
