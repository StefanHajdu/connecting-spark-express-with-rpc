<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Drawer, Button, CloseButton } from "flowbite-svelte";
import { sineIn } from "svelte/easing";
import { previewState } from "$lib/stores";
import DataFrameTable from "./DataFrameTable/DataFrameTable.svelte";

let title: string = "(footer)";
let backdrop = false;
let activateClickOutside = false;
let transitionParamsBottom = {
  y: 320,
  duration: 200,
  easing: sineIn,
};

function closePreview() {
  previewState.update((previewState) => {
    return { ...previewState, previewHidden: true };
  });
}

function openPreview() {
  previewState.update((previewState) => {
    return { ...previewState, previewHidden: false };
  });
}
</script>

<div class="sticky bottom-0">
  <footer class="p-1/2 flex items-center justify-between bg-gray-300">
    <p>{title}</p>
    <Button on:click={openPreview}>
      <AngleUpOutline />
    </Button>
    <Drawer
      placement="bottom"
      width="w-full"
      transitionType="fly"
      transitionParams={transitionParamsBottom}
      activateClickOutside={activateClickOutside}
      backdrop={backdrop}
      bind:hidden={$previewState.previewHidden}
      id="sidebar8"
      class="outline-1 outline-black">
      <div class="mb-2 flex h-6 items-center">
        <p>Preview</p>
        <CloseButton on:click={closePreview} class="dark:text-white" />
      </div>
      <DataFrameTable />
    </Drawer>
  </footer>
</div>
