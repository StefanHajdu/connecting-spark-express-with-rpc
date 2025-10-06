<script lang="ts">
import { Tabs } from "flowbite-svelte";
import { onMount } from "svelte";

import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import PreviewFooter from "../../components/PreviewFooter.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

onMount(async () => {
  await globalAnalysesState.setAnalysisFromAPI();
});
</script>

<div class="flex flex-col overflow-hidden h-screen">
  <Header />
  <Tabs defaultClass="sticky z-1 top-10 bg-[#fafafa]" contentClass="grow overflow-y-scroll">
    {#each globalAnalysesState.analyses as analysis, i (analysis.id)}
      <AnalysisSession analysisIndex={i} />
    {/each}
  </Tabs>
  <PreviewFooter />
</div>
