<script lang="ts">
import { Label, Input, Modal, Button } from "flowbite-svelte";
import { post } from "$lib/clientApi";
import { goto } from "$app/navigation";
import { AnalysisSession, globalAnalysesState } from "./AnalysisSessionClass.svelte";

let openNewAnalysisTabForm = $state(false);
let name = $state("");

async function initNewAnalysisTabForm() {
  // qa: when creating new analysis, on backend it means that only 1 session should be loaded
  // therefore it might be needed to delete all sesssion on this call
  let newAnalysis = new AnalysisSession({ name: name, selected: true });

  let createSessionResponse = await post("/rpc/session/create", {
    session_id: newAnalysis.session_id,
    name: newAnalysis.name,
  });
  if (createSessionResponse) {
    globalAnalysesState.analyses.push(newAnalysis);
    await goto("http://localhost:4444/analyses");
  }
}
</script>

<Button color="green" on:click={() => (openNewAnalysisTabForm = true)}>New Tab</Button>

<Modal bind:open={openNewAnalysisTabForm} size="xs" autoclose outsideclose>
  <div>
    <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create New Analysis</h3>
    <Label class="space-y-2">
      <span>Name your analysis:</span>
      <Input type="text" name="analysisName" placeholder="name" required bind:value={name} />
    </Label>

    <Button onclick={initNewAnalysisTabForm} class="w-full1">Create</Button>
  </div>
</Modal>
