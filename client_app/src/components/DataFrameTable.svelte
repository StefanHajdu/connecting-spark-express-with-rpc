<style>
.resizer {
  position: absolute;
  top: 0;
  height: 100%;
  width: 5px;
  background: rgba(0, 0, 0, 0.5);
  cursor: col-resize;
  user-select: none;
  touch-action: none;
}

.resizer.isResizing {
  background: blue;
  opacity: 1;
}

@media (hover: hover) {
  .resizer {
    opacity: 0;
  }

  *:hover > .resizer {
    opacity: 1;
  }
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
  type ColumnSizingInfoState,
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
let columnSizingInfo = $state<ColumnSizingInfoState>(previewObject.sizingInfoConf);

const table = createSvelteTable({
  data,
  columns,
  defaultColumn: {
    minSize: 50,
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
  onColumnSizingInfoChange: (updater) => {
    if (typeof updater === "function") {
      columnSizingInfo = updater(columnSizingInfo);
    } else {
      columnSizingInfo = updater;
    }
    previewObject.sizingInfoConf = columnSizingInfo;
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
    get columnSizingInfo() {
      return columnSizingInfo;
    },
  },
});

$inspect(columnSizing);
</script>

<div class="h-full overflow-y-auto overflow-x-scroll pb-4">
  <Table hoverable={true} style={`width: ${table.getCenterTotalSize()}px`}>
    <TableHead class="normal-case">
      {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
        {#each headerGroup.headers as header (header.id)}
          {#if !header.isPlaceholder}
            <TableHeadCell class="px-0 pl-2 text-normal border border-black text-xs relative" colspan={header.colSpan}>
              <div style={`width: ${header.getSize()}px;`}>
                <!-- header title  -->
                <div class="flex justify-between">
                  <div class="min-w-0">
                    <p class="truncate">
                      <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
                    </p>
                    <p class="truncate font-normal">
                      {header.column.columnDef.footer}
                    </p>
                  </div>

                  <!-- column menu  -->
                  <div>
                    <Button class="p-1 m-2 h-4 w-4"><ChevronDownOutline class="h-2 w-2" /></Button>
                    <Dropdown bind:open={columnMenu[header.column.columnDef.header as keyof typeof columnMenu].open}>
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

                <!-- resizer  -->
                <div
                  role="button"
                  tabindex="0"
                  ondblclick={() => {
                    header.column.resetSize();
                  }}
                  onmousedown={header.getResizeHandler()}
                  class={`resizer ${header.column.getIsResizing() ? "isResizing" : ""} right-0`}
                  style={`transform: translateX(${table.getState().columnSizingInfo.deltaOffset}px)`}>
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
              <div style={`width: ${cell.column.getSize()}px;`}>
                <p class="truncate">
                  <FlexRender content={cell.column.columnDef.cell} context={cell.getContext()} />
                </p>
              </div>
            </TableBodyCell>
          {/each}
        </TableBodyRow>
      {/each}
    </TableBody>
  </Table>
</div>
