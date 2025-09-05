<script lang="ts">
import { Table, TableBody, TableBodyRow, TableHead, TableBodyCell, TableHeadCell, Spinner } from "flowbite-svelte";
import type { Preview } from "../PreviewStore.svelte";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

interface Props {
    previewObject: Preview;
}

let { previewObject }: Props = $props();
let streamInProgress = $state(false);

export async function preview(analysisId: string, nodeId: string): Promise<void> {
    streamInProgress = true;
    await previewObject.run(analysisId, nodeId);
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
                {#each previewObject.columns as column}
                    <DataFrameTableHeadCell columnName={column.name} dType={column.type} />
                {/each}
            </TableHead>
            <TableBody>
                {#each previewObject.data as row, id}
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
