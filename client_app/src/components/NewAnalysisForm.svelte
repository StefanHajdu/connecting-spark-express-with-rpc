<script lang="ts">
import { Label, Input, Modal, Button } from "flowbite-svelte";
import { LS_KEY_ANALYSES, LS_KEY_SCOPED, toLocalStorage } from "$lib/localStorageHandles";
import { getUniqueAnalysesId } from "../lib/utils";
import { fetchSparkApi } from "$lib/clientApi";
import { goto } from "$app/navigation";
import type { Analysis } from "$lib/dtype";
import { nodeFactory } from "./Nodes/NodeClass.svelte";

interface Props {
    analyses: Analysis[];
}

let { analyses = $bindable() }: Props = $props();

let openNewAnalysisForm = $state(false);
let name = $state("");
let id = getUniqueAnalysesId();

async function initNewAnalysis() {
    let createSessionResponse = await fetchSparkApi("/rpc/session/create", {
        id: id,
        name: name,
    });
    if (createSessionResponse) {
        analyses.push({
            id: id,
            name: name,
            status: "new",
            buildTime: "---",
            resources: "---",
            rest: "...",
            selected: true,
            nodes: [nodeFactory("Load", [])],
        });

        toLocalStorage(
            LS_KEY_ANALYSES,
            analyses
                .filter((a) => a.selected)
                .map((a) => {
                    return {
                        ...a,
                        nodes: a.nodes.map((node) => node.getClassSnapshot()),
                    };
                }),
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
