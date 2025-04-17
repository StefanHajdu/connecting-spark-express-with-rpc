<script lang="ts">
	import { TableHeadCell } from 'flowbite-svelte';

	let { columnName, dType } = $props();
</script>

<TableHeadCell class="text- normal border border-black px-3 py-2 text-xs normal-case">
	<p class="w-32 truncate">{columnName}</p>
	<p class="w-32 truncate">{dType}</p>
</TableHeadCell>
