<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Drawer, Button, CloseButton, Spinner } from "flowbite-svelte";
import { sineIn } from "svelte/easing";
import { footerPreview } from "./PreviewStore.svelte";
import DataFrameTable from "./DataFrameTable.svelte";

let title: string = "(footer)";
let backdrop = false;
let activateClickOutside = false;
let transitionParamsBottom = {
  y: 320,
  duration: 200,
  easing: sineIn,
};
let collapsed = $state(true);
let rerenderState = $derived.by(() => {
  return footerPreview.salt;
});

export async function preview(analysisId: string, nodeId: string): Promise<void> {
  collapsed = true;
  footerPreview.visibilityToggle(true);
  await footerPreview.run(analysisId, nodeId);
  collapsed = false;
}

$inspect(rerenderState);
</script>

<footer class="sticky bottom-0 p-1/2 flex items-center justify-between bg-gray-300">
  <p>{title}</p>

  <Button
    on:click={() => {
      collapsed = false;
      footerPreview.visibilityToggle(!collapsed);
    }}>
    <AngleUpOutline />
  </Button>
  {#key rerenderState}
    <Drawer
      placement="bottom"
      width="w-full"
      transitionType="fly"
      transitionParams={transitionParamsBottom}
      activateClickOutside={activateClickOutside}
      backdrop={backdrop}
      bind:hidden={collapsed}
      id="sidebar8"
      class="outline-1 outline-black">
      <div class="mb-2 flex h-6 items-center">
        <div class="mb-2">
          <p>Preview</p>
          <div class="flex justify-normal">
            <p class="font-normal text-xs">{footerPreview.data.length} rows,</p>
            <p class="ml-1 font-semibold text-xs">{footerPreview.columns.length} columns</p>
          </div>
        </div>

        <CloseButton
          on:click={() => {
            collapsed = true;
            footerPreview.visibilityToggle(!collapsed);
          }}
          class="dark:text-white" />
      </div>
      <DataFrameTable previewObject={footerPreview} />
    </Drawer>
  {/key}
</footer>
