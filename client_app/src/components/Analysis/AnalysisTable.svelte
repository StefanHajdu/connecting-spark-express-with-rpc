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
import { AnalysisSession } from "./AnalysisSessionClass.svelte";
import { goto } from "$app/navigation";

interface Props {
  persistedAnalyses: AnalysisSession[];
}

let { persistedAnalyses = $bindable() }: Props = $props();

let globalCheck = $derived.by(() => {
  return persistedAnalyses.every((a) => a.selected);
});

function checkboxAnalyses(analyses: AnalysisSession[], flag: boolean): void {
  for (let i = 0; i < analyses.length; i++) {
    analyses[i].setSelected(flag);
  }
}
</script>

<div>
  <Button size="xs" color="red" disabled={true}>Delete</Button>
</div>
<Table hoverable={true}>
  <TableHead>
    <TableHeadCell class="p-4!">
      <form autocomplete="off">
        <Checkbox
          checked={globalCheck}
          onchange={() => {
            globalCheck = !globalCheck;
            checkboxAnalyses(persistedAnalyses, globalCheck);
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
    {#each persistedAnalyses as analysis, i (analysis.session_id)}
      <TableBodyRow>
        <TableBodyCell class="p-4!">
          <form autocomplete="off">
            <Checkbox
              checked={analysis.selected}
              onchange={() => {
                analysis.setSelected(!analysis.selected);
              }} />
          </form>
        </TableBodyCell>
        <TableBodyCell>{analysis.name}</TableBodyCell>
        <TableBodyCell>{analysis.nodes ? analysis.nodes.length : 0}</TableBodyCell>
        <TableBodyCell>{analysis.status}</TableBodyCell>
        <TableBodyCell>{analysis.buildTime}</TableBodyCell>
        <TableBodyCell>{analysis.resources}</TableBodyCell>
        <TableHeadCell>
          <!-- button open -->
          <Button
            size="xs"
            color="blue"
            disabled={false}
            onclick={() => {
              void goto("http://localhost:4444/analyses");
            }}>Open</Button>
        </TableHeadCell>
      </TableBodyRow>
    {/each}
  </TableBody>
</Table>
