<script lang="ts">
import {
  Table,
  TableBody,
  TableBodyRow,
  TableHead,
  TableBodyCell,
  TableHeadCell,
} from "flowbite-svelte";
import { lastPreviewedRows } from "$lib/stores";
import { actionState, finishAction } from "$lib/actionState.svelte";
import { fetchSparkApi } from "$lib/clientApi";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

$effect(() => {
  if (actionState.inProgress) {
    fetchSparkApi("preview", {
      session_id: actionState.analysiId,
      node_id: actionState.currNode,
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
});

$inspect(actionState);
</script>

<div class="h-80 overflow-y-auto">
  <Table>
    <TableHead>
      <TableHeadCell class="text- normal border border-black px-3 py-2 text-xs"
      ></TableHeadCell>
      {#each actionState.columns as column}
        <DataFrameTableHeadCell columnName={column.name} dType={column.dtype} />
      {/each}
    </TableHead>
    <TableBody>
      {#each $lastPreviewedRows as row, id}
        <TableBodyRow>
          <TableBodyCell
            class="text- normal border border-black px-3 py-2 text-xs"
            >{id + 1}</TableBodyCell>
          {#each Object.values(row) as rowValue}
            <DataFrameTableCell value={rowValue} />
          {/each}
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</div>
