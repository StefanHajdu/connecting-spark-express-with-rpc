<script lang="ts">
import { Dropdown, DropdownItem, DropdownHeader, DropdownDivider, Button } from "flowbite-svelte";
import { ChevronDownOutline, CloseOutline, FileCopyOutline } from "flowbite-svelte-icons";
import Icon from "@iconify/svelte";
import { v4 as uuidv4 } from "uuid";
import { AnalysisSession } from "../../Analysis/AnalysisSessionClass.svelte";
import ExpressionFrom from "./ExpressionFrom.svelte";
import { sparkColumnFunctions } from "$lib/sparkColumnFunction";
import type { Expression } from "$lib/dtype";
import { compileExprString, compileExprObj } from "$lib/utils";

interface Props {
    analyses: AnalysisSession[];
    analysisIndex: number;
    nodeIndex: number;
}
let { analyses = $bindable(), analysisIndex, nodeIndex }: Props = $props();

let expressions: Expression[] = $state([]);
let exprSelectionOpen = $state(false);

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

$inspect(expressions);

function duplicateExpr(exprId: number) {
    const exprToDuplicate = structuredClone($state.snapshot(expressions)[exprId]);
    exprToDuplicate.newColumnName = "new_" + exprToDuplicate.newColumnName;
    exprToDuplicate.uuid = "add_col_expr-" + uuidv4();
    expressions.splice(exprId + 1, 0, exprToDuplicate);
}

function removeExpr(exprId: number) {
    expressions.splice(exprId, 1);
}

async function submit() {
    await analyses[analysisIndex].submitNode(analyses[analysisIndex].nodes[nodeIndex], {
        session_id: analyses[analysisIndex].id,
        node_id: analyses[analysisIndex].nodes[nodeIndex].id,
        prev_node_id: analyses[analysisIndex].nodes[nodeIndex].prevNodeId,
        expressions: expressions.map((expr: any) => compileExprObj(expr)),
    });
}
</script>

<h5 class="mb-1 text-xl font-medium text-gray-900 dark:text-white">
    {analyses[analysisIndex].nodes[nodeIndex].title}
</h5>
<span class="text-sm text-gray-500 dark:text-gray-400">Add Column</span>
{#each expressions as expr, i (expr.uuid)}
    <div class="mb-4">
        <div class="flex items-stretch">
            <ExpressionFrom
                bind:exprs={expressions}
                idx={i}
                columnsOnNodeInput={analyses[analysisIndex].nodes[nodeIndex].columnsOnNodeInput} />
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
    <Button disabled={!analyses[analysisIndex].nodes[nodeIndex].active} onclick={submit}>Submit</Button>
</div>
