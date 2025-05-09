<script lang="ts">
import { Label, Select, MultiSelect, Input, Toggle } from "flowbite-svelte";

let { exprs = $bindable(), idx, colsInDf } = $props();
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
                bind:value={exprs[idx].params[jdx].value} />
            </Label>
          {:else}
            <Label class="text-black-600/75"
              >{param["name"]}
              <Select
                size="sm"
                items={colsInDf
                  .filter((col: any) => {
                    return exprs[idx].sparkTypes.has(col.dtype);
                  })
                  .map((col: any) => {
                    return { value: col.name, name: col.name };
                  })}
                bind:value={exprs[idx].params[jdx].value} />
            </Label>
          {/if}
          <Toggle size="small" class="pt-1" bind:checked={customInputChecked} />
        </div>
      {:else if param.ptype === "multi_col"}
        <Label class="text-black-600/75"
          >{param["name"]}
          <MultiSelect
            size="sm"
            items={colsInDf.map((col: any) => {
              return { value: col.name, name: col.name };
            })}
            bind:value={multiColSelection}
            on:change={(event) => (exprs[idx].params[jdx].value = multiColSelection.join(", "))} />
        </Label>
      {:else}
        <Label class="text-black-600/75"
          >{param["name"]}
          <Input type={param.ptype} size="sm" placeholder="..." bind:value={exprs[idx].params[jdx].value} />
        </Label>
      {/if}
    {/each}
  </div>
  <div class="col-span-2 col-start-11">
    <Label class="text-black-600/75"
      >new column name
      <Input type="text" size="md" placeholder="..." bind:value={exprs[idx].rename} />
    </Label>
  </div>
</div>
