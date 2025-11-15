<script lang="ts">
import { Label, Select, MultiSelect, Input, Toggle } from "flowbite-svelte";
import type { Column } from "$lib/dtype";
import { AddColumnExpression } from "./Expression.svelte";
import type { SparkType } from "./Expression.svelte";

interface Props {
  exprs: AddColumnExpression[];
  idx: number;
  columnsOnNodeInput: Column[];
}
const multiColSelection: string[] = [];

let { exprs = $bindable(), idx, columnsOnNodeInput }: Props = $props();
</script>

<div class="mt-4 grid gap-3 md:grid-cols-12">
  <div class="mt-7 col-span-2">
    <p class="font-mono text-xs">{exprs[idx].name}()</p>
  </div>
  <div class="col-span-7 col-start-3 grid gap-2 md:grid-cols-3">
    {#each exprs[idx].args as arg, jdx}
      {#if arg.arg.selector === "single"}
        <div>
          {#if exprs[idx].args[jdx].valueField.customInputUsed}
            <Label class="text-black-600/75"
              >value
              {#if arg.arg.custom_input !== "nan" && arg.arg.custom_input !== "any"}
                <input
                  type={arg.arg.custom_input}
                  value={exprs[idx].args[jdx].valueField.value ? exprs[idx].args[jdx].valueField.value : ""}
                  class="bg-neutral-secondary-medium border border-default-medium text-heading text-sm rounded-base focus:ring-brand focus:border-brand block w-full px-1.5 py-1 shadow-xs placeholder:text-body"
                  placeholder="..."
                  oninput={(event) => {
                    exprs[idx].args[jdx].valueField.value = event.currentTarget.value;
                  }} />
              {/if}
            </Label>
          {:else}
            <Label class="text-black-600/75"
              >{arg.arg.name}
              <Select
                class="text-[12px] px-1 py-0.5"
                placeholder="Columns..."
                value={exprs[idx].args[jdx].valueField.value}
                items={columnsOnNodeInput
                  .filter((col: Column) => {
                    return arg.arg.spark_types.includes(col.dtype as SparkType);
                  })
                  .map((col: any) => {
                    return { value: col.name, name: col.name };
                  })}
                oninput={(event) => {
                  exprs[idx].args[jdx].valueField.value = event.currentTarget.value;
                }} />
            </Label>
          {/if}
          <Toggle size="small" class="pt-1" bind:checked={exprs[idx].args[jdx].valueField.customInputUsed} />
        </div>
      {:else}
        <Label class="text-black-600/75"
          >{arg.arg.name}
          <MultiSelect
            placeholder="Columns..."
            class="text-[12px] px-1.5 py-0.5"
            items={columnsOnNodeInput.map((col: any) => {
              return { value: col.name, name: col.name };
            })}
            bind:value={exprs[idx].args[jdx].valueField.value as (string | number)[]} />
        </Label>
      {/if}
    {/each}
  </div>
  <div class="col-span-2 col-start-11">
    <Label class="text-black-600/75"
      >new column
      <Input type="text" class="text-[12px] px-1 py-0.5" placeholder="..." bind:value={exprs[idx].newColumnName} />
    </Label>
  </div>
</div>
