<script lang="ts">
import { Label, Select, MultiSelect, Input } from "flowbite-svelte";

let { exprs = $bindable(), idx, colsInDf } = $props();
let multiColSelection = $state([]);
</script>

<div class="mt-4 grid gap-3 md:grid-cols-12">
  <div class="mt-7 col-span-2">
    <p class="font-mono text-sm">{exprs[idx]["fname"]}()</p>
  </div>
  <div class="col-span-7 col-start-3 grid gap-2 md:grid-cols-3">
    {#each exprs[idx]["params"] as param, jdx}
      <Label
        >{param["name"]}
        {#if param.ptype === "single_col"}
          <Select
            size="sm"
            items={colsInDf.map((col: any) => {
              return { value: col.name, name: col.name };
            })}
            bind:value={exprs[idx].params[jdx].value} />
        {:else if param.ptype === "multi_col"}
          <MultiSelect
            size="sm"
            items={colsInDf.map((col: any) => {
              return { value: col.name, name: col.name };
            })}
            bind:value={multiColSelection}
            on:change={(event) => (exprs[idx].params[jdx].value = multiColSelection.join(", "))} />
        {:else}
          <Input type={param.ptype} size="sm" placeholder="..." bind:value={exprs[idx].params[jdx].value} />
        {/if}
      </Label>
    {/each}
  </div>
  <div class="col-span-2 col-start-11">
    <Label
      >new column name
      <Input type="text" size="sm" placeholder="..." bind:value={exprs[idx].rename} />
    </Label>
  </div>
</div>
