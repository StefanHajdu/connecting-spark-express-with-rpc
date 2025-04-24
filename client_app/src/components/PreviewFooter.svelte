<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Drawer, Button, CloseButton } from "flowbite-svelte";
import { sineIn } from "svelte/easing";
import { actionState } from "$lib/actionState.svelte";
import DataFrameTable from "./DataFrameTable/DataFrameTable.svelte";

let title: string = "(footer)";
let backdrop = false;
let activateClickOutside = false;
let transitionParamsBottom = {
  y: 320,
  duration: 200,
  easing: sineIn,
};
</script>

<div class="sticky bottom-0">
  <footer class="p-1/2 flex items-center justify-between bg-gray-300">
    <p>{title}</p>
    <Button
      on:click={() => {
        actionState.hidden = false;
      }}>
      <AngleUpOutline />
    </Button>
    <Drawer
      placement="bottom"
      width="w-full"
      transitionType="fly"
      transitionParams={transitionParamsBottom}
      activateClickOutside={activateClickOutside}
      backdrop={backdrop}
      bind:hidden={actionState.hidden}
      id="sidebar8"
      class="outline-1 outline-black">
      <div class="mb-2 flex h-6 items-center">
        <p>Preview</p>
        <CloseButton
          on:click={() => {
            actionState.hidden = true;
          }}
          class="dark:text-white" />
      </div>
      <DataFrameTable />
    </Drawer>
  </footer>
</div>
