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
import { STORAGE_KEY_ANALYSES, STORAGE_KEY_SELECTED_ANALYSES, toLocalStorage } from "../lib/localStorageHandles";
import { type AnalysesMock } from "$lib/analyses";

let analyses = $props();
let allAnalyses: AnalysesMock = $state(analyses[STORAGE_KEY_ANALYSES]);
let globalCheck = $derived.by(() => {
    return Object.keys(allAnalyses).every((key: string) => allAnalyses[key].selected === true);
});

function checkAllAnalyses(analyses: any, flag: boolean): AnalysesMock {
    let keys = Object.keys(analyses);
    for (let key of keys) {
        analyses[key].selected = flag;
    }
    return analyses;
}

function scopeSelected(): undefined {
    const scoped = [];
    for (const [key, value] of Object.entries(allAnalyses)) {
        if (value.selected) {
            scoped.push(key);
        }
    }
    toLocalStorage(STORAGE_KEY_SELECTED_ANALYSES, scoped);
}
</script>

<div>
    <Button size="xs" color="blue" onclick={scopeSelected} href="analyses">Open</Button>
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
                        allAnalyses = checkAllAnalyses(allAnalyses, globalCheck);
                        toLocalStorage(STORAGE_KEY_ANALYSES, allAnalyses);
                    }} />
            </form>
        </TableHeadCell>
        <TableHeadCell>Name</TableHeadCell>
        <TableHeadCell>Status</TableHeadCell>
        <TableHeadCell>Build Time</TableHeadCell>
        <TableHeadCell>Resources</TableHeadCell>
        <TableHeadCell>...</TableHeadCell>
    </TableHead>

    <TableBody tableBodyClass="divide-y">
        {#each Object.keys(allAnalyses) as key}
            <TableBodyRow>
                <TableBodyCell class="p-4!">
                    <form autocomplete="off">
                        <Checkbox
                            checked={allAnalyses[key].selected}
                            onchange={() => {
                                allAnalyses[key].selected = !allAnalyses[key].selected;
                                toLocalStorage(STORAGE_KEY_ANALYSES, allAnalyses);
                            }} />
                    </form>
                </TableBodyCell>
                <TableBodyCell>{allAnalyses[key].name}</TableBodyCell>
                <TableBodyCell>{allAnalyses[key].status}</TableBodyCell>
                <TableBodyCell>{allAnalyses[key].buildTime}</TableBodyCell>
                <TableBodyCell>{allAnalyses[key].resources}</TableBodyCell>
                <TableBodyCell>{allAnalyses[key].rest}</TableBodyCell>
            </TableBodyRow>
        {/each}
    </TableBody>
</Table>
