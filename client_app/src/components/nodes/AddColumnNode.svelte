<script lang="ts">
import { Input, Button } from "flowbite-svelte";
import { Node } from "./NodeInstance";

let { analysiId, nodesInAnalysis = $bindable(), nodeIndex, formFields = $bindable() } = $props();
let node: Node = nodesInAnalysis[nodeIndex];
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
