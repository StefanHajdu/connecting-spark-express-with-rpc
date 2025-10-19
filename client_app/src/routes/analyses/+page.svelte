<script lang="ts">
import { onMount } from "svelte";

import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import PreviewFooter from "../../components/PreviewFooter.svelte";
import NewAnalysisTabForm from "../../components/Analysis/NewAnalysisTabForm.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

let selectedIndex = $state(0);

onMount(async () => {
  await globalAnalysesState.setAnalysisFromAPI();
});

$effect(() => {
  const analyses = globalAnalysesState.analyses;

  if (!analyses.length) {
    selectedIndex = 0;
    return;
  }

  const flagged = analyses.findIndex((analysis) => analysis.selected);
  if (flagged >= 0) {
    selectedIndex = flagged;
  } else if (selectedIndex >= analyses.length) {
    selectedIndex = analyses.length - 1;
  }
});

function selectAnalysis(index: number) {
  globalAnalysesState.analyses.forEach((analysis, idx) => {
    analysis.selected = idx === index;
  });
  selectedIndex = index;
}
</script>

<div class="flex h-screen flex-col overflow-hidden">
  <Header />

  <div class="sticky z-10 flex items-center gap-4 px-4 py-3">
    <div class="tab-scroll flex-1 overflow-x-auto whitespace-nowrap">
      <div class="inline-flex items-center gap-4">
        {#each globalAnalysesState.analyses as analysis, i (analysis.session_id)}
          <button
            type="button"
            class={`text-slate-600 hover:text-slate-900 ${selectedIndex === i ? "text-slate-900 underline" : ""}`}
            onclick={() => selectAnalysis(i)}>
            {analysis.name}
          </button>
        {/each}
      </div>
    </div>
    <NewAnalysisTabForm />
  </div>

  <div class="flex-1 overflow-hidden">
    {#if globalAnalysesState.analyses.length}
      <AnalysisSession analysisIndex={selectedIndex} />
    {:else}
      <div class="flex h-full items-center justify-center">No analyses yet. Create one to get started.</div>
    {/if}
  </div>

  <PreviewFooter />
</div>

<style>
:global(html, body) {
  height: 100%;
  overflow: hidden;
}

.tab-scroll {
  scrollbar-width: none;
}

.tab-scroll::-webkit-scrollbar {
  display: none;
}
</style>
