<script lang="ts">
import { AngleUpOutline } from "flowbite-svelte-icons";
import { Drawer, Button, CloseButton } from "flowbite-svelte";
import { sineIn } from "svelte/easing";
import { tick } from "svelte";
import { onMount } from "svelte";
import { footerPreview } from "./PreviewStore.svelte";
import DataFrameTable from "./DataFrameTable/DataFrameTable.svelte";

onMount(() => {
    footerPreview.reset();
});

let title: string = "(footer)";
let backdrop = false;
let activateClickOutside = false;
let transitionParamsBottom = {
    y: 320,
    duration: 200,
    easing: sineIn,
};
let componentCollapsed = $state(true);
let dataframeTableComponent: any;

export async function forwardPreview(analysiId: string, nodeId: string): Promise<void> {
    componentCollapsed = false;
    tick().then(async () => {
        await dataframeTableComponent.preview(analysiId, nodeId);
    });
}
</script>

<footer class="sticky bottom-0 p-1/2 flex items-center justify-between bg-gray-300">
    <p>{title}</p>
    <Button
        on:click={() => {
            componentCollapsed = false;
        }}>
        <AngleUpOutline />
    </Button>
    <Drawer
        placement="bottom"
        width="w-full"
        transitionType="fly"
        transitionParams={transitionParamsBottom}
        activateClickOutside={activateClickOutside}
        backdrop={backdrop}
        bind:hidden={componentCollapsed}
        id="sidebar8"
        class="outline-1 outline-black">
        <div class="mb-2 flex h-6 items-center">
            <p>Preview</p>
            <CloseButton
                on:click={() => {
                    componentCollapsed = true;
                }}
                class="dark:text-white" />
        </div>
        <DataFrameTable bind:this={dataframeTableComponent} previewObject={footerPreview} />
    </Drawer>
</footer>
