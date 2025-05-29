<script lang="ts">
import { Dropdown, DropdownItem, DropdownHeader, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline, CloseOutline, FileCopyOutline } from "flowbite-svelte-icons";
import Icon from "@iconify/svelte";
import { v4 as uuidv4 } from "uuid";
import { Node, AddColumnNode } from "../NodeInstance.svelte";
import ExpressionFrom from "./ExpressionFrom.svelte";
import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import { fetchSparkApi } from "$lib/clientApi";
import type { SparkTransformResponse, Expression, Param } from "$lib/dtype";
import { compileExprString, compileExprObj, syncNodeColsOnAdd, getActivePredecessor } from "$lib/utils";

interface Props {
  nodesInAnalysis: Node[];
  nodeIndex: number;
  analysisId: string;
  activeNodeStatus: boolean;
}

let { analysisId, nodesInAnalysis = $bindable(), nodeIndex, activeNodeStatus }: Props = $props();
let node: Node = nodesInAnalysis[nodeIndex];
let expressions: Expression[] = $state([]);
let exprSelectionOpen = $state(false);
let msg = $state("");

function addExpression(category: string, fname: string) {
  // @ts-ignore
  let expr = sparkColumnFunctions[category].exprs[fname];
  expressions.push({
    uuid: "add_col_expr-" + uuidv4(),
    fname: fname,
    params: expr["params"].map((param: any) => {
      return { ...param, valueField: { value: "", source: "input" } };
    }),
    newColumnName: "",
    // @ts-ignore
    sparkTypes: new Set(sparkColumnFunctions[category].sparkTypes),
    // @ts-ignore
    customInput: sparkColumnFunctions[category].customInput,
  });
  exprSelectionOpen = false;
}

function duplicateExpr(exprId: number) {
  const exprToDuplicate = structuredClone($state.snapshot(expressions)[exprId]);
  exprToDuplicate.newColumnName = "new_" + exprToDuplicate.newColumnName;
  expressions.splice(exprId + 1, 0, exprToDuplicate);
}

function removeExpr(exprId: number) {
  expressions.splice(exprId, 1);
}

async function submit() {
  const colsAdded = new Set(expressions.map((expr: Expression) => expr.newColumnName));
  const colsUsed = new Set(
    expressions
      .flatMap((expr: Expression) => {
        return expr.params
          .filter((param: Param) => {
            return param.valueField.source === "col" || param.valueField.source === "cols";
          })
          .map((param: Param) => {
            if (param.valueField.source === "cols") {
              return typeof param.valueField.value === "string" ? param.valueField.value.split(",") : undefined;
            } else {
              return typeof param.valueField.value === "string" ? param.valueField.value : undefined;
            }
          });
      })
      .flat(),
  );

  const expressionsCompiled = expressions.map((expr: any) => compileExprObj(expr));

  let transformResponse: SparkTransformResponse = await fetchSparkApi("submitNode/NewColumnNode", {
    session_id: analysisId,
    node_id: nodesInAnalysis[nodeIndex].uuid,
    prev_node_id: nodesInAnalysis[getActivePredecessor(nodesInAnalysis, nodeIndex)].uuid,
    expressions: expressionsCompiled,
  });

  if (nodesInAnalysis[nodeIndex] instanceof AddColumnNode) {
    nodesInAnalysis[nodeIndex].expressions = expressionsCompiled;
  }

  if (transformResponse) {
    msg = transformResponse.msg;
    nodesInAnalysis[nodeIndex].colsInTransform = nodesInAnalysis[nodeIndex].colsInNode = transformResponse.columns;
    nodesInAnalysis[nodeIndex].colsAdded = colsAdded;
    nodesInAnalysis[nodeIndex].colsUsed = colsUsed;
    syncNodeColsOnAdd(nodesInAnalysis, nodeIndex);
  }
}
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
  {node.title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
{#each expressions as expr, i (expr.uuid)}
  <div class="mb-4">
    <div class="flex items-stretch">
      <ExpressionFrom
        bind:exprs={expressions}
        idx={i}
        colsInPrevDf={nodesInAnalysis[getActivePredecessor(nodesInAnalysis, nodeIndex)].colsInNode}
        nodeIndex={nodeIndex} />
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
    <p class="mt-2 font-mono text-xs">{compileExprString(expressions[i])}</p>
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
    {#each Object.keys(sparkColumnFunctions["numeric"].exprs) as fname}
      <DropdownItem onclick={() => addExpression("numeric", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:text-fields" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Text</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["string"].exprs) as fname}
      <DropdownItem onclick={() => addExpression("string", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:calendar-clock-outline-rounded" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Date/Time</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["date"].exprs) as fname}
      <DropdownItem onclick={() => addExpression("date", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:data-array" style="font-size: 24px" />
        <p class="dark:text-white ml-2">Array</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["array"].exprs) as fname}
      <DropdownItem onclick={() => addExpression("array", fname)}>{fname}</DropdownItem>
    {/each}
    <DropdownDivider />

    <DropdownHeader class="outline">
      <div class="flex items-stretch">
        <Icon icon="material-symbols-light:regular-expression-rounded" style="font-size: 24px" />
        <p class="dark:text-white">Miscellaneous</p>
      </div>
    </DropdownHeader>
    {#each Object.keys(sparkColumnFunctions["misc"].exprs) as fname}
      <DropdownItem onclick={() => addExpression("misc", fname)}>{fname}</DropdownItem>
    {/each}
  </Dropdown>
</div>
<div class="flex space-x-3 mt-2 rtl:space-x-reverse">
  <Button disabled={!activeNodeStatus} onclick={submit}>Submit</Button>
</div>
