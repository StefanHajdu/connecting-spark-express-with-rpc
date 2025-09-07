<script lang="ts">
import { Table, TableBody, TableBodyRow, TableHead, TableBodyCell, TableHeadCell, Spinner } from "flowbite-svelte";
import type { Preview } from "../PreviewStore.svelte";
import DataFrameTableHeadCell from "./DataFrameTableHeadCell.svelte";
import DataFrameTableCell from "./DataFrameTableCell.svelte";

import { type ColumnDef, getCoreRowModel } from "@tanstack/table-core";
import { createSvelteTable, FlexRender } from "$lib/components/data-table/index.js";

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

// ---------

const previewOutput = {
    data: [
        [
            "icatholic.org",
            "org",
            "f",
            "Name106, Inc.",
            "2004-09-23T00:00:00.000",
            "{ns3171.dns.dyn.com.,ns1141.dns.dyn.com.,ns2196.dns.dyn.com.,ns4169.dns.dyn.com.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
        [
            "blueadvise.com",
            "com",
            "f",
            "GoDaddy.com, LLC",
            "2021-09-13T00:00:00.000",
            "{ns1.namefind.com.,ns2.namefind.com.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
        [
            "thomas-ds.com",
            "com",
            "f",
            "Squarespace Domains LLC",
            "2022-08-11T00:00:00.000",
            "{dns1.p08.nsone.net.,dns2.p08.nsone.net.,dns3.p08.nsone.net.,dns4.p08.nsone.net.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
        [
            "modaiyun.com",
            "com",
            "f",
            "DNSPod, Inc.",
            "2020-07-06T00:00:00.000",
            "{f1g1ns1.dnspod.net.,f1g1ns2.dnspod.net.}",
            "{}",
            "{}",
            "2024-10-26T00:00:00.000",
        ],
        [
            "anivizzion.nl",
            "nl",
            "t",
            "unknown",
            null,
            "{een.dnssrv.nl.,drie.dnssrv.nl.,twee.dnssrv.nl.}",
            '"{""48274 RSASHA256 2 ee86077399af35f3510fd9aee5fe2a4d8c15a3f8c8a2bb25a10d78e3273e486b""}"',
            '"{""256 3 RSASHA256 AwEAAbfSGdIIZg7lyUI0Bf/1kHqgHOkG2f7+yjXYdd/5B4p1b8BEX1VfJPQvwctmvkzoIn0suflZ0S7iPosI7iRSa8sufyJoOi6CCQORDcOQ7JSOhTQG+c5yagm8CCWtjxLqfIkCg4vfh/1+kH+dFUNc43/oNspVyfxAc5/6lUOaHvBz"",""257 3 RSASHA256 AwEAAcUdaOOMBDlURspiQhHHAtmIqDvpXu/Qtbub24VcZYk7MgoquNPhkwAp6N6JdtFZz6tPzapYYqa0wRrzAMcn7i35xI2TDfb2Mrt+GvZfG5jU4+9+Vr7vtRHDuaFF92MtJxOu3VXzj8MqIJEPQbvqj/3nL0J4/ufRFKkz8kvd8s+xCqR5SEJn1F9750BSrrZJ+SW2Xb54J6HWvW4ZdqH8yKliICa9XeqBpYkqq+ATtrjoX2Ydxu+Wusq39IKPGbCE66fZhArVBVBnzqn+9vSXvNBXOWmwfJ7zpOcn1Ye74kKJtmxnyuB8GX5VLSwVCULcV33CqltUd8BzYXezZBP0umU=""}"',
            "2024-11-12T00:00:00.000",
        ],
        [
            "borntospeak.nl",
            "nl",
            "t",
            "ZXCS Vondellaan 47 2332AA Leiden Netherlands SIDN BV",
            "2023-07-16T00:00:00.000",
            "{ns.zxcs.be.,ns.zxcs.eu.,ns.zxcs.nl.}",
            '"{""712 ECDSAP256SHA256 2 89e79f39410e8956d430c6894496dad2a7082f45c5101d9d28a11574f5bf0b71""}"',
            '"{""257 3 ECDSAP256SHA256 fjAU8pdtY2PJOn5PUOLLuI1b4ZWSkvdvI62hHmXvAdSilGLIMTi16z2BdYr/Epot3Id3F3Hqno9HuWaukj8JkA==""}"',
            "2024-11-10T00:00:00.000",
        ],
        [
            "vkdh.nl",
            "nl",
            "t",
            "unknown",
            null,
            "{ns0.transip.net.,ns1.transip.nl.,ns2.transip.eu.}",
            '"{""40865 ECDSAP256SHA256 2 ec215d529ea46a91d80f06efc1fd250efd8a569683df74d672c966c7aa4e6853""}"',
            '"{""256 3 ECDSAP256SHA256 nvPvdeok2kgkwFhKhfITCXxeB79zjPBsX+B5DC68zyXHXGoEw7Y6G54GmhjaDg6Ay+pQC4yH7Yl323bzZtVqCg=="",""257 3 ECDSAP256SHA256 By9px81v653cQC3tbkWR+zToqrHPmd2C8liug+CmFWrwI+UD40GmJno8oSlbt+VQfU2icWtLqxFTVkizfLg5nw==""}"',
            "2024-11-12T00:00:00.000",
        ],
        [
            "tinkertoysrentals.com",
            "com",
            "f",
            "GoDaddy.com, LLC",
            "2022-05-20T00:00:00.000",
            "{wave.rental.software.,nap.rental.software.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
        [
            "art-life-etc.com",
            "com",
            "f",
            "Wix.com Ltd.",
            "2020-07-20T00:00:00.000",
            "{ns7.wixdns.net.,ns6.wixdns.net.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
        [
            "ingcliente-soportes.com",
            "com",
            "f",
            "Sav.com, LLC",
            "2024-08-27T00:00:00.000",
            "{ns1.all-harmless.domains.,ns2.all-harmless.domains.}",
            "{}",
            "{}",
            "2024-10-12T00:00:00.000",
        ],
    ],
    columns: [
        {
            name: "domain",
            type: "string",
        },
        {
            name: "tld",
            type: "string",
        },
        {
            name: "dnssec",
            type: "string",
        },
        {
            name: "registrar",
            type: "string",
        },
        {
            name: "created_at",
            type: "date",
        },
        {
            name: "records_ns",
            type: "string",
        },
        {
            name: "records_ds",
            type: "string",
        },
        {
            name: "records_dnskey",
            type: "string",
        },
        {
            name: "analyzed_at",
            type: "date",
        },
    ],
};

const data: (string | null)[][] = previewOutput.data;
const columns: ColumnDef<string | null>[] = previewOutput.columns.map((col, index) => {
    return { accessorKey: `${index}`, header: `${col.name}` };
});

const table = createSvelteTable({
    // @ts-ignore
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
});

console.log(table.getHeaderGroups());
console.log(table.getRowModel());
</script>

<div class="h-80 overflow-y-auto">
    <Table hoverable={true}>
        <TableHead>
            {#each table.getHeaderGroups() as headerGroup (headerGroup.id)}
                {#each headerGroup.headers as header (header.id)}
                    {#if !header.isPlaceholder}
                        <TableHeadCell class="text- normal border border-black px-3 py-2 text-xs">
                            <FlexRender content={header.column.columnDef.header} context={header.getContext()} />
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
