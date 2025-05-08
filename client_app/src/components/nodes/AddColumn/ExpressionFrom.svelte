<script lang="ts">
import { Label, Input, Dropdown, DropdownItem, DropdownDivider, Button } from "flowbite-svelte";

let { exprs = $bindable(), idx } = $props();
</script>

<div class="mt-4 grid w-full items-end gap-6 md:grid-cols-3">
  <Label>{exprs[idx]["fname"]}</Label>
  <div class="grid w-full items-end gap-3 md:grid-cols-3">
    {#each exprs[idx]["params"] as param, jdx}
      <Label
        >{param["name"]}
        <Input type="text" size="sm" placeholder="..." bind:value={exprs[idx].params[jdx].value} />
      </Label>
    {/each}
  </div>
  <Label
    >new column name
    <Input type="text" size="sm" placeholder="..." bind:value={exprs[idx].rename} />
  </Label>
</div>
