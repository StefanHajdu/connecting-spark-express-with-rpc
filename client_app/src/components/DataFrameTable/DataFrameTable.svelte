<script>
	import {
		Table,
		TableBody,
		TableBodyRow,
		TableHead,
		TableBodyCell,
		TableHeadCell
	} from 'flowbite-svelte';
	import DataFrameTableHeadCell from './DataFrameTableHeadCell.svelte';
	import DataFrameTableCell from './DataFrameTableCell.svelte';
</script>

<div class="h-80 overflow-y-auto">
	<Table>
		<TableHead>
			<TableHeadCell class="text- normal border border-black px-3 py-2 text-xs"></TableHeadCell>
			<DataFrameTableHeadCell
				columnName={'Let me share my experience in case it helps someone else to avoid the frustration. In my case the built-in truncate flag worked and the code looks like below'}
				dType={'string'}
			/>
			<DataFrameTableHeadCell columnName={'Color'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'Category'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'ACCESSORIES'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'AVAILABLE'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'Price'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'WEIGHT'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_1'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_2'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_3'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_4'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_1'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_2'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_3'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_4'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_1'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_2'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_3'} dType={'string'} />
			<DataFrameTableHeadCell columnName={'OVERFLOW_4'} dType={'string'} />
		</TableHead>
		<TableBody>
			{#each { length: 20 }, r}
				<TableBodyRow>
					<TableBodyCell class="text- normal border border-black px-3 py-2 text-xs"
						>{r + 1}</TableBodyCell
					>
					<DataFrameTableCell value={'Apple MacBook Pro 17'} />
					<DataFrameTableCell value={'Sliver'} />
					<DataFrameTableCell value={'Laptop'} />
					<DataFrameTableCell value={'Yes'} />
					<DataFrameTableCell value={'Yes'} />
					<DataFrameTableCell value={'$2999'} />
					<DataFrameTableCell value={'3.0 lb.'} />
					<DataFrameTableCell value={'3.0 lb.'} />
					<DataFrameTableCell value={'3.0 lb.'} />
					<DataFrameTableCell value={'3.0 lb.'} />
					<DataFrameTableCell value={'3.0 lb.'} />
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
</div>
