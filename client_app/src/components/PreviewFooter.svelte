<script lang="ts">
	import { AngleUpOutline } from 'flowbite-svelte-icons';
	import { Drawer, Button, CloseButton, A } from 'flowbite-svelte';
	import { sineIn } from 'svelte/easing';
	import DataFrameTable from './DataFrameTable/DataFrameTable.svelte';

	let title: string = '(footer)';
	let hidden8 = true;
	let backdrop = false;
	let activateClickOutside = false;
	let transitionParamsBottom = {
		y: 320,
		duration: 200,
		easing: sineIn
	};
</script>

<div class="sticky bottom-0">
	<footer class="p-1/2 flex items-center justify-between bg-gray-300">
		<p>{title}</p>
		<Button on:click={() => (hidden8 = false)}>
			<AngleUpOutline />
		</Button>
		<Drawer
			placement="bottom"
			width="w-full"
			transitionType="fly"
			transitionParams={transitionParamsBottom}
			{activateClickOutside}
			{backdrop}
			bind:hidden={hidden8}
			id="sidebar8"
			class="outline-1 outline-black"
		>
			<div class="mb-2 flex h-6 items-center">
				<p>Preview</p>
				<CloseButton on:click={() => (hidden8 = true)} class="dark:text-white" />
			</div>
			<DataFrameTable />
		</Drawer>
	</footer>
</div>
