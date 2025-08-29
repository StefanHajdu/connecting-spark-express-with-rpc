<script lang="ts">
import { Label, Input, Modal, Button } from "flowbite-svelte";
import { post } from "$lib/clientApi";
import { goto } from "$app/navigation";
import { AnalysisSession } from "./AnalysisSessionClass.svelte";

let openNewAnalysisForm = $state(false);
let name = $state("");

async function initNewAnalysis() {
    let newAnalysis = new AnalysisSession({ name: name, selected: true });

    let createSessionResponse = await post("/rpc/session/create", {
        id: newAnalysis.id,
        name: newAnalysis.name,
    });
    if (createSessionResponse) {
        await goto("http://localhost:5173/analyses");
    }
}
</script>

<Button color="green" on:click={() => (openNewAnalysisForm = true)}>New Analysis</Button>

<Modal bind:open={openNewAnalysisForm} size="xs" autoclose outsideclose>
    <div>
        <h3 class="mb-4 text-xl font-medium text-gray-900 dark:text-white">Create New Analysis</h3>
        <Label class="space-y-2">
            <span>Name your analysis:</span>
            <Input type="text" name="analysisName" placeholder="name" required bind:value={name} />
        </Label>

        <Button onclick={initNewAnalysis} class="w-full1">Create</Button>
    </div>
</Modal>
