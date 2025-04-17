<script lang="ts">
	import Header from '../components/Header.svelte';
	import Footer from '../components/Footer.svelte';
	import NewAnalysisForm from '../components/NewAnalysisForm.svelte';
	import AnalysisTable from '../components/AnalysisTable.svelte';
	import type { PageProps } from './$types';
	import { LS_KEY_ANALYSES, toLocalStorage } from '$lib/localStorageHandles';

	let { data }: PageProps = $props();
	let analyses = data;
	toLocalStorage(LS_KEY_ANALYSES, analyses);
</script>

<div class="grid h-screen grid-rows-[auto_1fr_auto]">
	<Header />

	<main class="bg-white-500 space-y-4 p-4">
		<div>
			<NewAnalysisForm {analyses} />
		</div>
		<div>
			<AnalysisTable {analyses} />
		</div>
	</main>

	<Footer />
</div>
