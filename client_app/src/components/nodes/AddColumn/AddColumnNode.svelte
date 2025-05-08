<script lang="ts">
import { Dropdown, DropdownItem, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline } from "flowbite-svelte-icons";
import { Node } from "../NodeInstance";
import ExpressionFrom from "./ExpressionFrom.svelte";
import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import { compileExpr } from "$lib/utils";

let { analysiId, nodesInAnalysis = $bindable(), nodeIndex, formFields = $bindable() } = $props();
let node: Node = nodesInAnalysis[nodeIndex];
let expressions: any[] = $state([]);
let exprSelectionOpen = $state(false);

function addExpression(category: string, fname: string) {
  // @ts-ignore
  let expr = sparkColumnFunctions[category][fname];
  expressions.push({
    fname: fname,
    params: expr["params"].map((param: any) => {
      return { ...param, value: "" };
    }),
    rename: "",
  });
  exprSelectionOpen = false;
}

async function submit() {}

$inspect(expressions);
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
{#each expressions as _, i}
  <ExpressionFrom bind:exprs={expressions} idx={i} colsInDf={nodesInAnalysis[nodeIndex].colsInDf} />
  <span>{compileExpr(expressions[i], nodesInAnalysis[nodeIndex].colsInDf)}</span>
{/each}
<div class="mt-4 flex justify-center">
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
<div class="flex space-x-3 mt-2 rtl:space-x-reverse">
  <Button on:click={submit}>Submit</Button>
</div>
