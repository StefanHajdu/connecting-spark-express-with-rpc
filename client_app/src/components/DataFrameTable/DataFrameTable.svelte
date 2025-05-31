<script lang="ts">
import { Table, TableBody, TableBodyRow, TableHead, TableBodyCell, TableHeadCell, Spinner } from "flowbite-svelte";
import { lastPreviewedRows } from "$lib/stores";
import { actionState, finishAction } from "$lib/actionState.svelte";
import { fetchSparkApi } from "$lib/clientApi";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

let pr = $state("Empty preview Request");

export function preview(previewRequest: string) {
  console.log(`From dataframeTable: ${previewRequest}`);
  pr = previewRequest;
}

let previewPromise = $derived.by(() => {
  if (actionState.confirmed) {
    return fetchSparkApi("preview", {
      session_id: actionState.analysiId,
      node_id: actionState.nodeId,
      limit: 1000,
    }).then((previewResponse) => {
      let parsed = previewResponse.row_json.map((row: string) => {
        return JSON.parse(JSON.parse(row));
      });

      finishAction();
      lastPreviewedRows.update(() => {
        return parsed;
      });
    });
  }
  return "preview";
});
</script>

<p>{pr}</p>

<!-- {#await previewPromise}
  <Spinner size="6" />
{:then _}
  <div class="h-80 overflow-y-auto">
    <Table>
      <TableHead>
        <TableHeadCell class="text- normal border border-black px-3 py-2 text-xs"></TableHeadCell>
        {#each actionState.columns as column}
          <DataFrameTableHeadCell columnName={column.name} dType={column.dtype} />
        {/each}
      </TableHead>
      <TableBody>
        {#each $lastPreviewedRows as row, id}
          <TableBodyRow>
            <TableBodyCell class="text- normal border border-black px-3 py-2 text-xs">{id + 1}</TableBodyCell>
            {#each Object.values(row) as rowValue}
              <DataFrameTableCell value={rowValue} />
            {/each}
          </TableBodyRow>
        {/each}
      </TableBody>
    </Table>
  </div>
{/await} -->
