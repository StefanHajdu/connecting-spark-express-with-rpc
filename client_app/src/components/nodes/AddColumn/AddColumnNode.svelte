<script lang="ts">
import { Dropdown, DropdownItem, DropdownHeader, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline } from "flowbite-svelte-icons";
import { Node } from "../NodeInstance";
import ExpressionFrom from "./ExpressionFrom.svelte";
import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import { compileExpr } from "$lib/utils";
import Icon from "@iconify/svelte";

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
  <div class="mb-4">
    <ExpressionFrom bind:exprs={expressions} idx={i} colsInDf={nodesInAnalysis[nodeIndex].colsInDf} />
    <p class="mt-2 font-mono text-xs">{compileExpr(expressions[i], nodesInAnalysis[nodeIndex].colsInDf)}</p>
  </div>
{/each}
<div class="mt-4 flex justify-center">
  <Button outline color="dark" class="px-5 py-0.25"
    >Add expression<ChevronDownOutline class="h-5 w-5 text-alternate dark:text-white" /></Button>

  <Dropdown bind:open={exprSelectionOpen}>
    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:123-rounded" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Numeric</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["numerical"]) as fname}
      <DropdownItem onclick={() => addExpression("numerical", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:text-fields" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Text</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["string"]) as fname}
      <DropdownItem onclick={() => addExpression("string", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:calendar-clock-outline-rounded" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Date/Time</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["date"]) as fname}
      <DropdownItem onclick={() => addExpression("date", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:data-array" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Array</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["array"]) as fname}
      <DropdownItem onclick={() => addExpression("array", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:regular-expression-rounded" style="font-size: 24px" />
        <p class="dark:text-white">Miscellaneous</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["misc"]) as fname}
      <DropdownItem onclick={() => addExpression("misc", fname)}>{fname}</DropdownItem>
    {/each}
  </Dropdown>
</div>
<div class="flex space-x-3 mt-2 rtl:space-x-reverse">
  <Button on:click={submit}>Submit</Button>
</div>
