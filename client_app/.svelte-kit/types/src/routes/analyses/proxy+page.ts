// @ts-nocheck
import type { PageLoad } from "./$types";
import { textBufferSparkStreamingApi } from "$lib/clientApi";

export const load = async ({ fetch, params }: Parameters<PageLoad>[0]) => {
    const streamingResponse = await fetch("http://localhost:4444/rpc/load/sessions");
    const objs = await textBufferSparkStreamingApi(streamingResponse);
    return {
        analyses: JSON.parse(objs),
    };
};
