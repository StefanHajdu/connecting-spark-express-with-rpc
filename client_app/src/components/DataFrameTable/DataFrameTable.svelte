<script lang="ts">
import { onMount, onDestroy } from "svelte";
import { Table, TableBody, TableBodyRow, TableHead, TableBodyCell, TableHeadCell } from "flowbite-svelte";
import type { Preview } from "../PreviewStore.svelte";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

import { type ColumnDef, getCoreRowModel, type SortingState, getSortedRowModel } from "@tanstack/table-core";
import { createSvelteTable, FlexRender } from "$lib/components/data-table/index.js";

interface Props {
    previewObject: Preview;
}

let { previewObject }: Props = $props();

onMount(() => {
    console.log("table entered DOM");
});

onDestroy(() => {
    console.log(`table left DOM`);
});

const data: (string | null)[][] = previewObject.data;
const columns: ColumnDef<string | null>[] = previewObject.columns.map((col, index) => {
    return { accessorKey: `${index}`, header: `${col.name}` };
});

let sorting = $state<SortingState>([]);
const table = createSvelteTable({
    // @ts-ignore
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    onSortingChange: (updater) => {
        if (typeof updater === "function") {
            sorting = updater(sorting);
        } else {
            sorting = updater;
        }
    },
    state: {
        get sorting() {
            return sorting;
        },
    },
});
</script>

<div class="h-80 overflow-y-auto">
    <Table hoverable={true}>
        <TableHead>
            {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
                {#each headerGroup.headers as header (header.id)}
                    {#if !header.isPlaceholder}
                        <TableHeadCell class="text- normal border border-black px-3 py-2 text-xs">
                            <div
                                class:cursor-pointer={header.column.getCanSort()}
                                class:select-none={header.column.getCanSort()}
                                on:click={header.column.getToggleSortingHandler()}>
                                <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
                                {#if header.column.getIsSorted().toString() === "asc"}
                                    🔼
                                {:else if header.column.getIsSorted().toString() === "desc"}
                                    🔽
                                {/if}
                            </div>
                        </TableHeadCell>
                    {/if}
                    <!-- <DataFrameTableHeadCell columnName={column.name} dType={column.type} /> -->
                {/each}
            {/each}
        </TableHead>
        <TableBody>
            {#each table.getRowModel().rows as row (row.id)}
                <TableBodyRow>
                    {#each row.getVisibleCells() as cell (cell.id)}
                        <TableBodyCell class="text- normal border border-black px-3 py-2 text-xs">
                            <p class="ml-1 h-1/4 w-32 truncate">
                                <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
                            </p>
                        </TableBodyCell>
                    {/each}
                </TableBodyRow>
            {/each}
        </TableBody>
    </Table>
</div>

<!-- {#if streamInProgress}
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
{/if} -->
