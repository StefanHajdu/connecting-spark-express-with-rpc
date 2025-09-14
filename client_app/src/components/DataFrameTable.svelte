<style>
.resizable {
  resize: inline;
  overflow: hidden;
  min-width: 120px;
  max-width: 470px;
}
</style>

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
import type { Preview } from "./PreviewStore.svelte";

import {
  type ColumnDef,
  type SortingState,
  type ColumnPinningState,
  type ColumnSizingState,
  getCoreRowModel,
  getSortedRowModel,
} from "@tanstack/table-core";
import { createSvelteTable, FlexRender } from "$lib/components/data-table/index.js";
import type { PreviewColumn } from "$lib/dtype";

interface Props {
  previewObject: Preview;
}

let { previewObject }: Props = $props();

type columnMenu = {
  open: boolean;
  pinning: string;
  asc: string;
  desc: string;
};
let columnMenuIsOpen = $state<Record<string, columnMenu>>(
  previewObject.columns.reduce((acc: Record<string, columnMenu>, col: PreviewColumn) => {
    return {
      ...acc,
      [col.name]: {
        open: false,
        pinning: "bg-white font-normal",
        asc: "bg-white font-normal",
        desc: "bg-white font-normal",
      },
    };
  }, {}),
);

onMount(() => {
  console.log("table entered DOM");
});

onDestroy(() => {
  console.log(`table left DOM`);
});

const data: (string | null)[][] = previewObject.data;
const columns: ColumnDef<(string | null)[] | null, any>[] = previewObject.columns.map((col, index) => {
  return { accessorKey: `${index}`, header: `${col.name}`, footer: `${col.type}` };
});

let sorting = $state<SortingState>([]);
let pinning = $state<ColumnPinningState>({});
let columnSizing = $state<ColumnSizingState>({});

const table = createSvelteTable({
  data,
  columns,
  defaultColumn: {
    size: 150,
    minSize: 150,
    maxSize: 500,
  },
  enableColumnResizing: true,
  columnResizeMode: "onChange",
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
      pinning = updater(pinning);
    } else {
      pinning = updater;
    }
  },
  onColumnSizingChange: (updater) => {
    console.log("sth is happening");
    if (typeof updater === "function") {
      columnSizing = updater(columnSizing);
    } else {
      columnSizing = updater;
    }
  },
  state: {
    get sorting() {
      return sorting;
    },
    get columnPinning() {
      return pinning;
    },
    get columnSizing() {
      return columnSizing;
    },
  },
});
</script>

<div class="h-80 overflow-y-auto">
  <Table hoverable={true} class="table-fixed">
    <TableHead class="normal-case">
      {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
        {#each headerGroup.headers as header (header.id)}
          {#if !header.isPlaceholder}
            <TableHeadCell
              class="text-normal border border-black text-xs"
              colspan={header.colSpan}
              style={`width:${header.getSize()}px`}>
              <div>
                <div
                  role="button"
                  tabindex="0"
                  ondblclick={() => {
                    header.column.resetSize();
                  }}
                  onmousedown={header.getResizeHandler()}
                  class="flex justify-between gap-1 resizable">
                  <div class="w-[70%]">
                    <p class="truncate">
                      <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
                    </p>
                    <p class="truncate font-normal">
                      {header.column.columnDef.footer}
                    </p>
                  </div>

                  <div>
                    <Button class="p-1 m-2 h-4 w-4"><ChevronDownOutline class="h-2 w-2" /></Button>
                    <Dropdown
                      bind:open={
                        columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].open
                      }>
                      <DropdownItem
                        class={columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].desc}
                        onclick={() => {
                          if (header.column.getIsSorted().toString() === "desc") {
                            header.getContext().column.clearSorting();

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].desc =
                              "bg-white font-normal";
                          } else {
                            header.getContext().table.setSorting([{ desc: true, id: header.getContext().column.id }]);

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].desc =
                              "bg-sky-100 font-semibold";
                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].asc =
                              "bg-white font-normal";
                          }

                          columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].open =
                            false;
                        }}>
                        <div class="flex justify-normal gap-2">
                          <Icon icon="tabler:sort-descending-small-big" width="16" height="16" />
                          <p>Sort descending</p>
                        </div></DropdownItem>

                      <DropdownItem
                        class={columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].asc}
                        onclick={() => {
                          if (header.column.getIsSorted().toString() === "asc") {
                            header.getContext().column.clearSorting();

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].asc =
                              "bg-white font-normal";
                          } else {
                            header.getContext().table.setSorting([{ desc: false, id: header.getContext().column.id }]);

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].asc =
                              "bg-sky-100 font-semibold";
                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].desc =
                              "bg-white font-normal";
                          }

                          columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].open =
                            false;
                        }}>
                        <div class="flex justify-normal gap-2">
                          <Icon icon="tabler:sort-ascending-small-big" width="16" height="16" />
                          <p>Sort ascending</p>
                        </div></DropdownItem>

                      <DropdownItem
                        class={columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen]
                          .pinning}
                        onclick={() => {
                          if (header.column.getIsPinned()) {
                            header.column.pin(false);

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].pinning =
                              "bg-white font-normal";
                          } else {
                            header.column.pin("left");

                            columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].pinning =
                              "bg-sky-100 font-semibold";
                          }

                          columnMenuIsOpen[header.column.columnDef.header as keyof typeof columnMenuIsOpen].open =
                            false;
                        }}>
                        <div class="flex justify-normal gap-2">
                          <Icon icon="tabler:pin" width="16" height="16" />
                          <p>Pin</p>
                        </div>
                      </DropdownItem>
                    </Dropdown>
                  </div>
                </div>
              </div>

              <div class="flex justify-normal gap-2">
                {#if header.column.getIsSorted().toString() === "asc"}
                  <div>
                    <Icon icon="tabler:sort-ascending-small-big" width="16" height="16" />
                  </div>
                {:else if header.column.getIsSorted().toString() === "desc"}
                  <div>
                    <Icon icon="tabler:sort-descending-small-big" width="16" height="16" />
                  </div>
                {/if}
                {#if header.column.getIsPinned()}
                  <div>
                    <Icon icon="tabler:pin" width="16" height="16" />
                  </div>
                {/if}
              </div>
            </TableHeadCell>
          {/if}
        {/each}
      {/each}
    </TableHead>
    <TableBody>
      {#each table.getRowModel().rows as row (row.id)}
        <TableBodyRow>
          {#each row.getVisibleCells() as cell (cell.id)}
            <TableBodyCell class="px-1 py-1 text-normal border border-black text-xs">
              <p class="truncate">
                <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
              </p>
            </TableBodyCell>
          {/each}
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</div>
