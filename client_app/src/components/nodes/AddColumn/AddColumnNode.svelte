<script lang="ts">
import { Dropdown, DropdownItem, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline } from "flowbite-svelte-icons";
import { Node } from "../NodeInstance";
import { sparkColumnFunctions } from "$lib/sparkColumnFunction";

let { analysiId, nodesInAnalysis = $bindable(), nodeIndex, formFields = $bindable() } = $props();
let node: Node = nodesInAnalysis[nodeIndex];
let expressions: any[] = $state([]);
let exprSelectionOpen = $state(false);

function addExpression(category: string, fname: string) {
  // @ts-ignore
  let expr = sparkColumnFunctions[category][fname];
  expressions.push(expr);
  exprSelectionOpen = false;
}

$inspect(expressions, exprSelectionOpen);
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
<div class="flex justify-center">
  <Button size="xs" color="blue"
    >Add expression<ChevronDownOutline class="ms-2 h-6 w-6 text-white dark:text-white" /></Button>
  <Dropdown bind:open={exprSelectionOpen}>
    {#each Object.keys(sparkColumnFunctions["numerical"]) as fname}
      <DropdownItem onclick={() => addExpression("numerical", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />
    {#each Object.keys(sparkColumnFunctions["string"]) as fname}
      <DropdownItem onclick={() => addExpression("string", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />
    {#each Object.keys(sparkColumnFunctions["date"]) as fname}
      <DropdownItem onclick={() => addExpression("date", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />
    {#each Object.keys(sparkColumnFunctions["array"]) as fname}
      <DropdownItem onclick={() => addExpression("array", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />
    {#each Object.keys(sparkColumnFunctions["misc"]) as fname}
      <DropdownItem onclick={() => addExpression("misc", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />
  </Dropdown>
</div>
