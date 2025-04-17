<script lang="ts">
	import { Label, Input, Modal, Button } from 'flowbite-svelte';
	import { LS_KEY_ANALYSES, LS_KEY_SCOPED, toLocalStorage } from '$lib/localStorageHandles';
	import { getUniqueAnalysesId } from '../lib/utils';

	let { analyses } = $props();

	let openNewAnalysisForm = $state(false);
	let name = $state('');

	function initNewAnalysis() {
		let id = getUniqueAnalysesId();
		analyses[id] = {
			id: id,
			name: name,
			status: 'new',
			buildTime: '---',
			resources: '---',
			rest: '...',
			selected: false
		};
		toLocalStorage(LS_KEY_ANALYSES, analyses);
		toLocalStorage(LS_KEY_SCOPED, [id]);

		postNewAnalysisCreated();
	}

	function postNewAnalysisCreated(): void {
		console.log(`POST /newSession ${name}`);
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
		<Button on:click={initNewAnalysis} class="w-full1" href="analyses">Create</Button>
	</div>
</Modal>
