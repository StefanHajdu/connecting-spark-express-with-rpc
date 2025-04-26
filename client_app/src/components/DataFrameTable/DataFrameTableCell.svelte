<script lang="ts">
	import { TableBodyCell } from 'flowbite-svelte';

	let { value } = $props();
</script>

<TableBodyCell class="text- normal px-3/2 border border-black py-1 text-xs normal-case">
	<p class="ml-1 h-1/4 w-32 truncate">{value}</p>
</TableBodyCell>
