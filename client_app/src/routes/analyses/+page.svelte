<script lang="ts">
import { Tabs, TabItem, CloseButton } from "flowbite-svelte";
import { onMount } from "svelte";
import { Pane, Splitpanes } from "svelte-splitpanes";

import Header from "../../components/Header.svelte";
import AnalysisSession from "../../components/Analysis/AnalysisSession.svelte";
import PreviewFooter from "../../components/PreviewFooter.svelte";
import { footerPreview } from "../../components/PreviewStore.svelte";
import { globalAnalysesState } from "../../components/Analysis/AnalysisSessionClass.svelte";
import DataFrameTable from "../../components/DataFrameTable.svelte";

let previewPaneSize = $state(0);

let previewPane;

let previewVisible = $derived.by(() => {
  return footerPreview.visible;
});

function handleResize(event: any) {
  previewPaneSize = Math.round(event.detail[1].size);
  footerPreview.visible = previewPaneSize > 0;
}

let rerenderState = $derived.by(() => {
  return footerPreview.salt;
});

onMount(async () => {
  await globalAnalysesState.setAnalysisFromAPI();
});

$inspect(previewPaneSize);
</script>

<div class="grid h-screen w-screen grid-rows-[auto_1fr_auto]">
  <!-- <Header /> -->
  <main class="bg-white-500 space-y-4 p-4">
    <Splitpanes horizontal={true} style="height: 95vh" on:resize={handleResize}>
      <Pane minSize={30} maxSize={100}>
        <div class="overflow-y-auto h-full bg-[#fafafa]">
          <Tabs tabStyle="pill" class="sticky top-0 z-10 bg-[#fafafa]">
            {#each globalAnalysesState.analyses as analysis, i (analysis.id)}
              <AnalysisSession analysisIndex={i} />
            {/each}
          </Tabs>
        </div>
      </Pane>
      <Pane snapSize={5} size={previewVisible ? 50 : 0}>
        <div class="bg-[#fafafa] h-[95%]">
          <div class="mt-2 mb-2 flex h-6 items-center">
            <div class="m-2">
              <p>Preview</p>
              <div class="flex justify-normal">
                <p class="font-normal text-xs">{footerPreview.data.length} rows,</p>
                <p class="ml-1 font-semibold text-xs">{footerPreview.columns.length} columns</p>
              </div>
            </div>

            <CloseButton
              on:click={() => {
                footerPreview.visibilityToggle(false);
              }}
              class="dark:text-white" />
          </div>
          {#key rerenderState}
            <DataFrameTable previewObject={footerPreview} />
          {/key}
        </div>
      </Pane>
    </Splitpanes>
  </main>
  <!-- <PreviewFooter /> -->
</div>
