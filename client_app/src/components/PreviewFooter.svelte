<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Button } from "flowbite-svelte";
import { footerPreview } from "./PreviewStore.svelte";

let title: string = "(footer)";

export async function preview(analysisId: string, nodeId: string): Promise<void> {
  footerPreview.visibilityToggle(true);
  await footerPreview.run(analysisId, nodeId);
}
</script>

<footer class="sticky bottom-0 p-1/2 flex items-center justify-between bg-gray-300">
  <p>{title}</p>

  <Button
    on:click={() => {
      footerPreview.visibilityToggle(true);
    }}>
    <AngleUpOutline />
  </Button>
</footer>
