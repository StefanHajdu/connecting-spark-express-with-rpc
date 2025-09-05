import type { PreviewColumn } from "$lib/dtype";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";

export class Preview {
    columns: PreviewColumn[] = $state([]);
    data: any[][] = $state([[]]);

    constructor() {
        this.columns = [];
        this.data = [];
    }

    public reset() {
        this.columns = [];
        this.data = [];
    }

    public sync(columns: PreviewColumn[], data: any[][]) {
        this.columns = columns;
        this.data = data;
    }

    public async run(analysisId: string, nodeId: string, limit: number = 1000): Promise<void> {
        const streamingResponse = await post("rpc/sessionNode/action/preview", {
            session_id: analysisId,
            node_id: nodeId,
            limit: limit,
        });

        const responseJson = await textBufferSparkStreamingApi(streamingResponse);
        const responseParsed: Preview = JSON.parse(responseJson);
        this.columns = responseParsed.columns;
        this.data = responseParsed.data;
    }
}

export class FooterPreview extends Preview {
    visible: boolean = $state(false);

    constructor() {
        super();
        this.visible = false;
    }

    public visibilityToggle(visible: boolean) {
        this.visible = visible;
    }

    public async run(analysisId: string, nodeId: string, limit: number = 1000): Promise<void> {
        if (this.visible) {
            super.run(analysisId, nodeId, limit);
        }
    }
}

export const footerPreview = $state(new FooterPreview());
