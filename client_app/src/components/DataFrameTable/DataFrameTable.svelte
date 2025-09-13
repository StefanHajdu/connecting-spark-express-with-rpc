<script lang="ts">
import { onMount, onDestroy } from "svelte";
import {
    Table,
    TableBody,
    TableBodyRow,
    TableHead,
    TableBodyCell,
    TableHeadCell,
    Dropdown,
    DropdownItem,
    Button,
} from "flowbite-svelte";
import Icon from "@iconify/svelte";
import { ChevronDownOutline } from "flowbite-svelte-icons";
import type { Preview } from "../PreviewStore.svelte";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

import {
    type ColumnDef,
    type SortingState,
    type ColumnPinningState,
    getCoreRowModel,
    getSortedRowModel,
} from "@tanstack/table-core";
import { createSvelteTable, FlexRender } from "$lib/components/data-table/index.js";

interface Props {
    previewObject: Preview;
}

let { previewObject }: Props = $props();
let columnMenuIsOpen = $state(false);

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
let columnPinning = $state<ColumnPinningState>({});

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
    onColumnPinningChange: (updater) => {
        if (typeof updater === "function") {
            columnPinning = updater(columnPinning);
        } else {
            columnPinning = updater;
        }
    },
    state: {
        get sorting() {
            return sorting;
        },
        get columnPinning() {
            return columnPinning;
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
                            <Button class="px-1 py-1"><ChevronDownOutline class="h-3 w-3" /></Button>
                            <Dropdown>
                                <DropdownItem
                                    onclick={() => {
                                        header
                                            .getContext()
                                            .table.setSorting([{ desc: true, id: header.getContext().column.id }]);
                                        columnMenuIsOpen = false;
                                    }}>desc</DropdownItem>
                                <DropdownItem
                                    onclick={() => {
                                        header
                                            .getContext()
                                            .table.setSorting([{ desc: false, id: header.getContext().column.id }]);
                                        columnMenuIsOpen = false;
                                    }}>asc</DropdownItem>
                                <DropdownItem
                                    onclick={() => {
                                        header.getContext().column.clearSorting();
                                        columnMenuIsOpen = false;
                                    }}>original</DropdownItem>
                                <DropdownItem
                                    onclick={() => {
                                        if (header.column.getIsPinned()) {
                                            header.column.pin(false);
                                        } else {
                                            header.column.pin("left");
                                        }
                                        columnMenuIsOpen = false;
                                    }}>pin left</DropdownItem>
                            </Dropdown>
                            <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
                            {#if header.column.getIsSorted().toString() === "asc"}
                                <Icon icon="tabler:sort-ascending-small-big" width="12" height="12" />
                            {:else if header.column.getIsSorted().toString() === "desc"}
                                <Icon icon="tabler:sort-descending-small-big" width="12" height="12" />
                            {/if}
                            {#if header.column.getIsPinned()}
                                <Icon icon="tabler:pin" width="12" height="12" />
                            {/if}
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
