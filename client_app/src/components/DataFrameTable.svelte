<style>
.resizable {
  resize: inline;
  overflow: hidden;
  min-width: 120px;
  max-width: 470px;
}
</style>

<script lang="ts">
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

type columnMenuType = {
  open: boolean;
};
let columnMenu = $state<Record<string, columnMenuType>>(
  previewObject.columns.reduce((acc: Record<string, columnMenuType>, col: PreviewColumn) => {
    return {
      ...acc,
      [col.name]: {
        open: false,
      },
    };
  }, {}),
);

const data: (string | null)[][] = previewObject.data;
const columns: ColumnDef<(string | null)[] | null, any>[] = previewObject.columns.map((col, index) => {
  return { accessorKey: `${index}`, header: `${col.name}`, footer: `${col.type}` };
});

let sorting = $state<SortingState>(previewObject.sortingConf);
let pinning = $state<ColumnPinningState>(previewObject.pinningConf);
let columnSizing = $state<ColumnSizingState>(previewObject.sizingConf);

const table = createSvelteTable({
  data,
  columns,
  defaultColumn: {
    size: 60,
    minSize: 60,
    maxSize: 500,
  },
  enableColumnResizing: true,
  columnResizeMode: "onEnd",
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  onSortingChange: (updater) => {
    if (typeof updater === "function") {
      sorting = updater(sorting);
    } else {
      sorting = updater;
    }
    previewObject.sortingConf = sorting;
  },
  onColumnPinningChange: (updater) => {
    if (typeof updater === "function") {
      pinning = updater(pinning);
    } else {
      pinning = updater;
    }
    previewObject.pinningConf = pinning;
  },
  onColumnSizingChange: (updater) => {
    if (typeof updater === "function") {
      columnSizing = updater(columnSizing);
    } else {
      columnSizing = updater;
    }
    previewObject.sizingConf = columnSizing;
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

<div class="h-full overflow-y-auto pb-4">
  <Table hoverable={true}>
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
                    <p class="w-32 truncate">
                      <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
                    </p>
                    <p class="w-32 truncate font-normal">
                      {header.column.columnDef.footer}
                    </p>
                  </div>

                  <div>
                    <Button class="p-1 m-2 h-4 w-4"><ChevronDownOutline class="h-2 w-2" /></Button>
                    <Dropdown bind:open={columnMenu[header.column.columnDef.header as keyof typeof columnMenu].open}>
                      <DropdownItem
                        class={header.column.getIsSorted().toString() === "desc"
                          ? "bg-sky-100 font-semibold"
                          : "bg-white font-normal"}
                        onclick={() => {
                          if (header.column.getIsSorted().toString() === "desc") {
                            header.getContext().column.clearSorting();
                          } else {
                            header.getContext().table.setSorting([{ desc: true, id: header.getContext().column.id }]);
                          }

                          columnMenu[header.column.columnDef.header as keyof typeof columnMenu].open = false;
                        }}>
                        <div class="flex justify-normal gap-2">
                          <Icon icon="tabler:sort-descending-small-big" width="16" height="16" />
                          <p>Sort descending</p>
                        </div></DropdownItem>

                      <DropdownItem
                        class={header.column.getIsSorted().toString() === "asc"
                          ? "bg-sky-100 font-semibold"
                          : "bg-white font-normal"}
                        onclick={() => {
                          if (header.column.getIsSorted().toString() === "asc") {
                            header.getContext().column.clearSorting();
                          } else {
                            header.getContext().table.setSorting([{ desc: false, id: header.getContext().column.id }]);
                          }

                          columnMenu[header.column.columnDef.header as keyof typeof columnMenu].open = false;
                        }}>
                        <div class="flex justify-normal gap-2">
                          <Icon icon="tabler:sort-ascending-small-big" width="16" height="16" />
                          <p>Sort ascending</p>
                        </div></DropdownItem>

                      <DropdownItem
                        class={header.column.getIsPinned() ? "bg-sky-100 font-semibold" : "bg-white font-normal"}
                        onclick={() => {
                          if (header.column.getIsPinned()) {
                            header.column.pin(false);
                          } else {
                            header.column.pin("left");
                          }

                          columnMenu[header.column.columnDef.header as keyof typeof columnMenu].open = false;
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
              <p class="w-32 truncate">
                <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
              </p>
            </TableBodyCell>
          {/each}
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</div>
