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
import { get } from "svelte/store";
import { previewState } from "$lib/stores";
import { fetchSparkStreamingApi } from "$lib/clientApi";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

let localPreviewState = $state(get(previewState));
let rowBuffer = $derived.by(async () => {
  let localBuffer: any[] = [];
  if (localPreviewState.previewInProgress === false) {
    const response = await fetchSparkStreamingApi("preview", {
      session_id: $previewState.analysiId,
      node_id: $previewState.nodeId,
      limit: 100,
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
  }
  return localBuffer;
});

$inspect(localPreviewState, rowBuffer);
</script>

{#await rowBuffer}
  <Spinner size={6} />
{:then rowBufferVal}
  <div class="h-80 overflow-y-auto">
    <Table>
      <TableHead>
        <TableHeadCell
          class="text- normal border border-black px-3 py-2 text-xs"
        ></TableHeadCell>
        {#each localPreviewState.columns as column}
          <DataFrameTableHeadCell
            columnName={column.name}
            dType={column.dtype} />
        {/each}
      </TableHead>
      <TableBody>
        {#each rowBufferVal
          .filter((r) => r !== "")
          .map((r) => JSON.parse(r)) as row, id}
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
