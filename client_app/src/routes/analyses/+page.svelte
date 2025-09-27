<script lang="ts">
import { Tabs, CloseButton } from "flowbite-svelte";
import { onMount } from "svelte";
import { Pane, Splitpanes } from "svelte-splitpanes";

import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import PreviewFooter from "../../components/PreviewFooter.svelte";
import { footerPreview } from "../../components/PreviewStore.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";

let previewVisible = $derived.by(() => {
  return footerPreview.visible;
});

onMount(async () => {
  await globalAnalysesState.setAnalysisFromAPI();
});
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
  <Header />

  <main class="bg-white-500 space-y-4 p-4">
    <!-- <Tabs defaultClass="bg-red-500 text-yellow-200">
      {#each globalAnalysesState.analyses as analysis, i (analysis.id)}
        <AnalysisSession analysisIndex={i} />
      {/each}
    </Tabs> -->

    <Splitpanes horizontal={true} style="height: full, overflow: hidden">
      <Pane minSize={20} maxSize={100}>
        <div class="overflow-auto h-full">
          <span> 1 </span>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
          <div class="specs">I have a min height of 20% &amp; max height of 70%</div>
        </div>
      </Pane>
      <Pane snapSize={5} size={previewVisible ? 40 : 0}>
        <div class="mt-2 mb-2 flex h-6 items-center">
          <span>
            3
            <br />
            <em class="specs">Table will be visible here</em>
          </span>
          <CloseButton
            on:click={() => {
              footerPreview.visibilityToggle(false);
            }}
            class="dark:text-white" />
        </div>
      </Pane>
    </Splitpanes>
  </main>
  <PreviewFooter />
</div>
