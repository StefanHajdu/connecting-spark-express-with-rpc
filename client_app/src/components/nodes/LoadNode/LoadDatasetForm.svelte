<script lang="ts">
import { Input, Button, Modal, Dropdown, DropdownItem, Toggle, Label } from "flowbite-svelte";
import { ChevronDownOutline } from "flowbite-svelte-icons";
import { type SparkTransformResponse, type Column } from "$lib/dtype";
import { fetchSparkApi } from "$lib/clientApi";
import { Node } from "../NodeInstance.svelte";

interface Props {
  analysisId: string;
  name: string;
  nodesInAnalysis: Node[];
  nodeIndex: number;
}

let { analysisId, name, nodesInAnalysis = $bindable(), nodeIndex }: Props = $props();
let loadDatasetModal = $state(false);

let inputTypeDropdownOpen: boolean = $state(false);
let inputType: string = $state("parquet");
let datasetPath: string = $state("");

// csv
let csvIncludeHeader: boolean = $state(true);
let csvDelimiter: string = $state(";");

// json
let jsonMultiline: boolean = $state(true);

async function submit() {
  let loadResponse: SparkTransformResponse = await fetchSparkApi("rpc/sessionNode/transform/submitLoadDatasetNode", {
    session_id: analysisId,
    [inputType]:
      inputType === "csv"
        ? { delimiter: csvDelimiter, include_header: csvIncludeHeader, path: datasetPath }
        : inputType === "json"
          ? { multiline: jsonMultiline, path: datasetPath }
          : inputType === "parquet"
            ? { path: datasetPath }
            : { path: datasetPath },
  });

  if (loadResponse) {
    nodesInAnalysis[nodeIndex].colsInTransform = nodesInAnalysis[nodeIndex].colsInNode = loadResponse.columns;
    nodesInAnalysis[nodeIndex].colsAdded = new Set(loadResponse.columns.map((col: Column) => col.name));
    loadDatasetModal = false;
  }
}
</script>

<div class="grid grid-cols-5 gap-4">
  <div class="col-span-4 col-start-3">
    <Button
      class="mt-2 mb-3"
      color="blue"
      onclick={() => {
        loadDatasetModal = true;
      }}>{name}</Button>
  </div>
</div>

<Modal title="Load Dataset" bind:open={loadDatasetModal}>
  <div class="mb-2">
    <Button>{inputType}<ChevronDownOutline class="h-3 w-3 text-white dark:text-white" /></Button>
    <Dropdown bind:open={inputTypeDropdownOpen}>
      <DropdownItem
        onclick={() => {
          inputType = "parquet";
          inputTypeDropdownOpen = false;
        }}>parquet</DropdownItem>
      <DropdownItem
        onclick={() => {
          inputType = "json";
          inputTypeDropdownOpen = false;
        }}>json</DropdownItem>
      <DropdownItem
        onclick={() => {
          inputType = "csv";
          inputTypeDropdownOpen = false;
        }}>csv</DropdownItem>
    </Dropdown>
  </div>

  {#if inputType === "csv"}
    <div class="grid grid-cols-10 gap-2 mt-2 mb-2">
      <div class="col-start-1 col-end-2">
        <Label>Delimiter</Label>
      </div>
      <div class="col-start-2 col-end-3">
        <Input size="sm" type="text" required bind:value={csvDelimiter} />
      </div>
      <div class="col-start-3 col-end-4">
        <Label>Include Header</Label>
      </div>
      <div class="col-start-4 col-end-5">
        <Toggle class="pt-1" bind:checked={csvIncludeHeader} />
      </div>
    </div>
  {/if}
  {#if inputType === "json"}
    <div class="grid grid-cols-10 gap-2 mt-2 mb-2">
      <div class="col-start-1 col-end-3">
        <Label>Multiline JSON</Label>
      </div>
      <div class="col-start-3 col-end-4">
        <Toggle class="pt-1" bind:checked={jsonMultiline} />
      </div>
    </div>
  {/if}

  <div class="mb-3">
    <Input type="text" id="first_name" placeholder="Enter absotule path..." required bind:value={datasetPath} />
  </div>

  {#if datasetPath !== ""}
    <Button color="blue" disabled={datasetPath === ""} on:click={submit}>Submit</Button>
  {/if}
</Modal>
