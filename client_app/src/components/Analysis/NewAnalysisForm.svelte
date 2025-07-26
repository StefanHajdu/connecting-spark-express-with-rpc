<script lang="ts">
import { Label, Input, Modal, Button } from "flowbite-svelte";
import { LS_KEY_ANALYSES, toLocalStorage } from "$lib/localStorageHandles";
import { fetchSparkApi } from "$lib/clientApi";
import { goto } from "$app/navigation";
import { AnalysisC } from "./AnalysisClass.svelte";

interface Props {
    analyses: AnalysisC[];
}

let { analyses = $bindable() }: Props = $props();

let openNewAnalysisForm = $state(false);
let name = $state("");

async function initNewAnalysis() {
    let analysisC = new AnalysisC({ selected: true });

    let createSessionResponse = await fetchSparkApi("/rpc/session/create", {
        id: analysisC.id,
        name: analysisC.name,
    });
    if (createSessionResponse) {
        analyses.push(analysisC);

        toLocalStorage(
            LS_KEY_ANALYSES,
            analyses.filter((analysis) => analysis.selected).map((analysis) => analysis.getSnapshot()),
        );

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
