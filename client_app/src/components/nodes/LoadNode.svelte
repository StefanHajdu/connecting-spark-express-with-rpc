<script lang="ts">
import { Input, Button } from "flowbite-svelte";
import { fetchLoadTransform } from "$lib/clientApi";

let { node, analysis_id } = $props();
let filePath: string = $state("");

let msg = $state("");
let dataFrameColumns = $state([{ name: "", dtype: "" }]);
let fileSize = $state(0);

// /home/stephenx/Documents/Programming/01_Blogs/contour-app/data/domains_small.parquet
async function submitLoad() {
  let loadResponse = await fetchLoadTransform("submitNode/LoadDatasetNode", {
    session_id: analysis_id,
    path: filePath,
  });

  if (loadResponse) {
    console.log(loadResponse);
    msg = loadResponse.transformResponse.msg;
    dataFrameColumns = loadResponse.transformResponse.columns;
    fileSize = loadResponse.size;
  }
}

$inspect(msg, dataFrameColumns, fileSize);
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
  <Button on:click={submitLoad}>Submit</Button>
</div>
