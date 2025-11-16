<script lang="ts">
import { Dropdown, DropdownItem, DropdownHeader, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline, CloseOutline, FileCopyOutline } from "flowbite-svelte-icons";
import Icon from "@iconify/svelte";
import { globalAnalysesState } from "../../Analysis/AnalysisSessionClass.svelte";
import ExpressionFrom from "../../Expression/AddColumnExpressionFrom.svelte";
import { AddColumnExpression } from "../../Expression/Expression.svelte";
import { exprs } from "../../Expression/ExpressionLib";

interface Props {
  analysisIndex: number;
  nodeIndex: number;
}
let { analysisIndex, nodeIndex }: Props = $props();

let expressions: AddColumnExpression[] = $state(
  globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].getUserInput().length > 0
    ? globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].getUserInput()
    : [],
);

$effect(() => {
  globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].setUserInput(expressions);
});

let exprSelectionOpen = $state(false);

function addExpression(name: string) {
  expressions.push(new AddColumnExpression({ name: name }));
  exprSelectionOpen = false;
}

function duplicateExpr(exprId: number) {
  const exprClone = expressions[exprId].clone();
  console.log(exprClone);
  expressions.splice(exprId + 1, 0, exprClone);
}

function removeExpr(exprId: number) {
  expressions.splice(exprId, 1);
}

async function submit() {
  await globalAnalysesState.analyses[analysisIndex].submitNode(
    globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex],
    {
      session_id: globalAnalysesState.analyses[analysisIndex].session_id,
      node_id: globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].node_id,
      prev_node_id: globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].prevNodeId,
    },
  );
}
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
{#each expressions as expr, i (expr.uuid)}
  <div class="mb-4">
    <div class="flex items-stretch">
      <ExpressionFrom
        bind:exprs={expressions}
        idx={i}
        columnsOnNodeInput={globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].columnsOnNodeInput} />
      <div class="mt-6 ml-4">
        <Button
          color="alternative"
          class="px-0.25 py-0.25"
          onclick={() => {
            removeExpr(i);
          }}><CloseOutline /></Button>
        <Button
          color="alternative"
          class="px-0.25 py-0.25"
          onclick={() => {
            duplicateExpr(i);
          }}><FileCopyOutline /></Button>
      </div>
    </div>
    <p class="mt-2 font-mono text-xs">{expressions[i].toString()}</p>
  </div>
{/each}
<div class="mt-4 flex justify-center">
  <Button outline color="dark" class="px-5 py-0.25"
    >Add expression<ChevronDownOutline class="h-5 w-5 text-alternate dark:text-white" /></Button>

  <Dropdown bind:open={exprSelectionOpen} class="h-48 w-48 overflow-y-auto py-1">
    {#each Object.keys(exprs) as exprName}
      <DropdownItem onclick={() => addExpression(exprName)}>{exprName}</DropdownItem>
    {/each}
  </Dropdown>
</div>
<div class="flex space-x-3 mt-2 rtl:space-x-reverse">
  <Button disabled={!globalAnalysesState.analyses[analysisIndex].nodes[nodeIndex].active} onclick={submit}
    >Submit</Button>
</div>
