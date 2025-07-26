<script lang="ts">
import { Label, Select, MultiSelect, Input, Toggle } from "flowbite-svelte";
import type { Expression, Column } from "$lib/dtype";

interface Props {
  exprs: Expression[];
  idx: number;
  colsInPrevDf: Column[];
  nodeIndex: number;
}

let { exprs = $bindable(), idx, colsInPrevDf, nodeIndex } = $props();
let multiColSelection = $state([]);
let customInputChecked = $state(false);
</script>

<div class="mt-4 grid gap-3 md:grid-cols-12">
  <div class="mt-7 col-span-2">
    <p class="font-mono text-sm">{exprs[idx]["fname"]}()</p>
  </div>
  <div class="col-span-7 col-start-3 grid gap-2 md:grid-cols-3">
    {#each exprs[idx]["params"] as param, jdx}
      {#if param.ptype === "single_col"}
        <div>
          {#if customInputChecked}
            <Label class="text-black-600/75"
              >value
              <Input
                type={exprs[idx].customInput}
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
                items={colsInPrevDf
                  .filter((col: any) => {
                    return exprs[idx].sparkTypes.has(col.dtype);
                  })
                  .map((col: any) => {
                    return { value: col.name, name: col.name };
                  })}
                oninput={(event) => {
                  exprs[idx].params[jdx].valueField.value = event.currentTarget.value;
                  exprs[idx].params[jdx].valueField.source = "col";
                }} />
            </Label>
          {/if}
          <Toggle size="small" class="pt-1" bind:checked={customInputChecked} />
        </div>
      {:else if param.ptype === "multi_col"}
        <Label class="text-black-600/75"
          >{param["name"]}
          <MultiSelect
            size="sm"
            items={colsInPrevDf.map((col: any) => {
              return { value: col.name, name: col.name };
            })}
            bind:value={multiColSelection}
            on:change={(event) => {
              exprs[idx].params[jdx].valueField.value = multiColSelection.join(", ");
              exprs[idx].params[jdx].valueField.source = "cols";
            }} />
        </Label>
      {:else}
        <Label class="text-black-600/75"
          >{param["name"]}
          <Input type={param.ptype} size="sm" placeholder="..." bind:value={exprs[idx].params[jdx].valueField.value} />
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
