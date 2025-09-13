<script lang="ts">
import { Table, TableBody, TableBodyRow, TableHead, TableBodyCell, TableHeadCell, Spinner } from "flowbite-svelte";
import { get } from "svelte/store";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";
import { lastDataframe } from "$lib/stores";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

let streamInProgress = $state(false);

export async function preview(analysisId: string, nodeId: string): Promise<void> {
    streamInProgress = true;
    const streamingResponse = await post("rpc/sessionNode/action/preview", {
        session_id: analysisId,
        node_id: nodeId,
        limit: 1000,
    });

    const validJson = await textBufferSparkStreamingApi(streamingResponse);
    lastDataframe.set(JSON.parse(validJson));
    streamInProgress = false;
}
</script>

{#if streamInProgress}
    <Spinner size="6" />
{:else}
    <div class="h-80 overflow-y-auto">
        <Table>
            <TableHead>
                <TableHeadCell class="text- normal border border-black px-3 py-2 text-xs"></TableHeadCell>
                {#each get(lastDataframe).columns as column}
                    <DataFrameTableHeadCell columnName={column.name} dType={column.type} />
                {/each}
            </TableHead>
            <TableBody>
                {#each get(lastDataframe).data as row, id}
                    <TableBodyRow>
                        <TableBodyCell class="text- normal border border-black px-3 py-2 text-xs"
                            >{id + 1}</TableBodyCell>
                        {#each Object.values(row) as rowValue}
                            <DataFrameTableCell value={rowValue} />
                        {/each}
                    </TableBodyRow>
                {/each}
            </TableBody>
        </Table>
    </div>
{/if}
