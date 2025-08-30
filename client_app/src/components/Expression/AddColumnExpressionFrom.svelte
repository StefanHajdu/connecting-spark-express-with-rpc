<script lang="ts">
import { Label, Select, MultiSelect, Input, Toggle } from "flowbite-svelte";
import type { Column } from "$lib/dtype";
import { AddColumnExpression } from "./Expression.svelte";

interface Props {
    exprs: AddColumnExpression[];
    idx: number;
    columnsOnNodeInput: Column[];
}

let { exprs = $bindable(), idx, columnsOnNodeInput }: Props = $props();
let multiColSelection = $state([]);
let customInputChecked = $state(false);
</script>

<div class="mt-4 grid gap-3 md:grid-cols-12">
    <div class="mt-7 col-span-2">
        <p class="font-mono text-sm">{exprs[idx].methodName}()</p>
    </div>
    <div class="col-span-7 col-start-3 grid gap-2 md:grid-cols-3">
        {#each exprs[idx]["params"] as param, jdx}
            {#if param.dtype === "single_col"}
                <div>
                    {#if customInputChecked || exprs[idx].params[jdx].valueField.source === "input"}
                        <Label class="text-black-600/75"
                            >value
                            <Input
                                type={exprs[idx].customInput}
                                value={exprs[idx].params[jdx].valueField.value
                                    ? exprs[idx].params[jdx].valueField.value
                                    : ""}
                                size="md"
                                placeholder="..."
                                oninput={(event) => {
                                    exprs[idx].params[jdx].valueField.value = event.currentTarget.value;
                                    exprs[idx].params[jdx].valueField.source = "input";
                                }} />
                        </Label>
                    {:else}
                        <Label class="text-black-600/75"
                            >{param["name"]}
                            <Select
                                size="sm"
                                value={exprs[idx].params[jdx].valueField.value}
                                items={columnsOnNodeInput
                                    .filter((col: any) => {
                                        return exprs[idx].allowedInputTypes.has(col.dtype);
                                    })
                                    .map((col: any) => {
                                        return { value: col.name, name: col.name };
                                    })}
                                oninput={(event) => {
                                    exprs[idx].params[jdx].valueField.value = event.currentTarget.value;
                                    exprs[idx].params[jdx].valueField.source = "column";
                                }} />
                        </Label>
                    {/if}
                    <Toggle size="small" class="pt-1" bind:checked={customInputChecked} />
                </div>
            {:else if param.dtype === "multi_col"}
                <Label class="text-black-600/75"
                    >{param["name"]}
                    <MultiSelect
                        size="sm"
                        items={columnsOnNodeInput.map((col: any) => {
                            return { value: col.name, name: col.name };
                        })}
                        bind:value={multiColSelection}
                        on:change={(event) => {
                            exprs[idx].params[jdx].valueField.value = multiColSelection.join(", ");
                            exprs[idx].params[jdx].valueField.source = "columns";
                        }} />
                </Label>
            {:else}
                <Label class="text-black-600/75"
                    >{param["name"]}
                    <Input
                        type={param.dtype}
                        size="sm"
                        placeholder="..."
                        bind:value={exprs[idx].params[jdx].valueField.value} />
                </Label>
            {/if}
        {/each}
    </div>
    <div class="col-span-2 col-start-11">
        <Label class="text-black-600/75"
            >new column name
            <Input type="text" size="md" placeholder="..." bind:value={exprs[idx].newColumnName} />
        </Label>
    </div>
</div>
