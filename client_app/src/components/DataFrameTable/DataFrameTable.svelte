<script lang="ts">
import {
  Table,
  TableBody,
  TableBodyRow,
  TableHead,
  TableBodyCell,
  TableHeadCell,
  Spinner,
} from "flowbite-svelte";
import { lastPreviewedRows } from "$lib/stores";
import { actionState, finishAction } from "$lib/actionState.svelte";
import { fetchSparkStreamingApi } from "$lib/clientApi";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

async function bufferPreview() {
  if (actionState.inProgress) {
    let localBuffer: any[] = [];
    const response = await fetchSparkStreamingApi("preview", {
      session_id: actionState.analysiId,
      node_id: actionState.currNode,
      limit: 1000,
    });

    if (response.ok && response.body) {
      const reader = response.body.getReader();
      try {
        while (true) {
          const { value, done } = await reader?.read();
          if (done) break;
          const text = new TextDecoder().decode(value);
          localBuffer.push(...text.split("<stream_chunk_done>"));
        }
      } finally {
        reader.releaseLock();
      }
    }
    finishAction();
    lastPreviewedRows.update(() => {
      return localBuffer;
    });
  }
}

function readRows(rowBuffer: string[]): any[] {
  let malformedBuffer: string = "";
  return rowBuffer
    .filter((r) => r !== "")
    .map((r) => {
      try {
        return JSON.parse(r);
      } catch (error) {
        malformedBuffer += r;
        try {
          let bufferedChunk = JSON.parse(malformedBuffer);
          malformedBuffer = "";
          return bufferedChunk;
        } catch (error) {}
      }
    })
    .filter(Boolean);
}

$inspect("Table", actionState);
</script>

{#await bufferPreview()}
  <Spinner size={6} />
{:then rowBufferFullfiled}
  <div class="h-80 overflow-y-auto">
    <Table>
      <TableHead>
        <TableHeadCell
          class="text- normal border border-black px-3 py-2 text-xs"
        ></TableHeadCell>
        {#each actionState.columns as column}
          <DataFrameTableHeadCell
            columnName={column.name}
            dType={column.dtype} />
        {/each}
      </TableHead>
      <TableBody>
        {#each readRows($lastPreviewedRows) as row, id}
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
{/await}
