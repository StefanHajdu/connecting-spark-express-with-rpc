import type { PreviewColumn } from "$lib/dtype";
import { v4 as uuidv4 } from "uuid";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";
import { type ColumnDef } from "@tanstack/table-core";

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

    public getColumnOptions(): ColumnDef<string | null>[] {
        return this.columns.map((col, index) => {
            return { accessorKey: `${index}`, header: `${col.name}` };
        });
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
    salt: string = $state(uuidv4());

    constructor() {
        super();
        this.visible = false;
        this.salt = uuidv4();
    }

    public visibilityToggle(visible: boolean) {
        this.visible = visible;
    }

    public async run(analysisId: string, nodeId: string, limit: number = 1000): Promise<void> {
        if (this.visible) {
            // preview can run also on node submit, but only if preview table is opened
            await super.run(analysisId, nodeId, limit);
            this.salt = uuidv4();
        }
    }
}

export const footerPreview = $state(new FooterPreview());
