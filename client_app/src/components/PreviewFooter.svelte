<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Button } from "flowbite-svelte";
import { footerPreview } from "./PreviewStore.svelte";

let title: string = "(footer)";
</script>

<footer class="flex-none sticky bottom-0 p-1 flex items-center justify-between bg-gray-300">
  <p>{title}</p>

  <Button
    on:click={() => {
      footerPreview.visibilityToggle(true);
    }}>
    <AngleUpOutline />
  </Button>
</footer>
