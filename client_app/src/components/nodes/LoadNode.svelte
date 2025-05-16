<script lang="ts">
import { Input, Button } from "flowbite-svelte";
import { fetchSparkApi } from "$lib/clientApi";
import { type SparkLoadFileResponse } from "$lib/dtype";
import { Node } from "./NodeInstance";

let { analysiId, nodesInAnalysis = $bindable(), nodeIndex } = $props();
let node: Node = nodesInAnalysis[nodeIndex];

let filePath: string = $state("");
let msg = $state("");
let fileSize = $state(0);

async function submit() {
  let loadResponse: SparkLoadFileResponse = await fetchSparkApi("submitNode/LoadDatasetNode", {
    session_id: analysiId,
    path: filePath,
  });

  if (loadResponse) {
    msg = loadResponse.transformResponse.msg;
    fileSize = loadResponse.size;
    nodesInAnalysis[nodeIndex].colsInDf = loadResponse.transformResponse.columns;
    nodesInAnalysis[nodeIndex].colsAdded = loadResponse.transformResponse.columns;
    nodesInAnalysis[nodeIndex].colsUsed = [];
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
  <Button on:click={submit}>Submit</Button>
</div>
