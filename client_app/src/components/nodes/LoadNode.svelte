<script lang="ts">
import { Input, Button } from "flowbite-svelte";

let { node } = $props();
let filePath: string = $state("");

$inspect(filePath);
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Load Node</span>

<div class="mb-3">
  <Input
    type="text"
    id="first_name"
    placeholder="Enter full path..."
    required
    bind:value={filePath} />
</div>

<div class="mt-4 flex space-x-3 lg:mt-6 rtl:space-x-reverse">
  <Button>Submit</Button>
</div>
