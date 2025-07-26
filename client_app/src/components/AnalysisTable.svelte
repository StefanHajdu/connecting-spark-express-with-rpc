<script lang="ts">
import {
    Table,
    TableBody,
    TableBodyCell,
    TableBodyRow,
    TableHead,
    TableHeadCell,
    Checkbox,
    Button,
} from "flowbite-svelte";
import type { Analysis } from "$lib/dtype";

interface Props {
    analyses: Analysis[];
}

let { analyses = $bindable() }: Props = $props();

let globalCheck = $derived.by(() => {
    return analyses.every((a) => a.selected);
});

function checkboxAnalyses(analyses: Analysis[], flag: boolean): Analysis[] {
    return analyses.map((analysis: Analysis) => {
        return { ...analysis, selected: flag };
    });
}
</script>

<div>
    <Button size="xs" color="blue" href="analyses">Open</Button>
    <Button size="xs" color="red">Delete</Button>
</div>
<Table hoverable={true}>
    <TableHead>
        <TableHeadCell class="p-4!">
            <form autocomplete="off">
                <Checkbox
                    checked={globalCheck}
                    onchange={() => {
                        globalCheck = !globalCheck;
                        ``;
                        analyses = checkboxAnalyses(analyses, globalCheck);
                    }} />
            </form>
        </TableHeadCell>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell># Nodes</TableHeadCell>
        <TableHeadCell>Status</TableHeadCell>
        <TableHeadCell>Build Time</TableHeadCell>
        <TableHeadCell>Resources</TableHeadCell>
        <TableHeadCell>...</TableHeadCell>
    </TableHead>

    <TableBody tableBodyClass="divide-y">
        {#each analyses as analysis}
            <TableBodyRow>
                <TableBodyCell class="p-4!">
                    <form autocomplete="off">
                        <Checkbox
                            checked={analysis.selected}
                            onchange={() => {
                                analysis.selected = !analysis.selected;
                            }} />
                    </form>
                </TableBodyCell>
                <TableBodyCell>{analysis.name}</TableBodyCell>
                <TableBodyCell>{analysis.nodes ? analysis.nodes.length : 0}</TableBodyCell>
                <TableBodyCell>{analysis.status}</TableBodyCell>
                <TableBodyCell>{analysis.buildTime}</TableBodyCell>
                <TableBodyCell>{analysis.resources}</TableBodyCell>
                <TableBodyCell>{analysis.rest}</TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>
