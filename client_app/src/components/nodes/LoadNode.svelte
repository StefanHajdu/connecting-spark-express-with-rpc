<script lang="ts">
import { Input, Button } from "flowbite-svelte";
import { type SparkLoadFileResponse, fetchSparkApi } from "$lib/clientApi";

let { analysiId, node, dataFrameColumns = $bindable(), formFields = $bindable() } = $props();
let filePath: string = $state("");

let msg = $state("");
let fileSize = $state(0);

// /home/stephenx/Documents/Programming/01_Blogs/contour-app/data/domains_small.parquet
async function submitLoad() {
  let loadResponse: SparkLoadFileResponse = await fetchSparkApi("submitNode/LoadDatasetNode", {
    session_id: analysiId,
    path: filePath,
  });

  if (loadResponse) {
    msg = loadResponse.transformResponse.msg;
    fileSize = loadResponse.size;
    dataFrameColumns = loadResponse.transformResponse.columns;
    formFields = new Map([["path", filePath]]);
  }
}
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Load Dataset</span>

<div class="mb-3">
  <Input type="text" id="first_name" placeholder="Enter full path..." required bind:value={filePath} />
</div>

<div class="flex space-x-3 mt-2 rtl:space-x-reverse">
  <Button on:click={submitLoad}>Submit</Button>
</div>
