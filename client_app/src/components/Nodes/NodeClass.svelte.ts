import { v4 as uuidv4 } from "uuid";
import type { Column, SparkTransform, InvalidState, ICsvMetadata, IJsonMetadata, IParquetMetadata } from "$lib/dtype";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";

const MASTER_NODE_ID = "0000-0000-0000";

export function nodeFactory(params: any): Node {
    if (params.title.toLowerCase() === "load") {
        return new LoadNode(params);
        // } else if (params.title.toLowerCase() === "filter") {
        //     return new FilterNode(params);
        // } else if (params.title.toLowerCase() === "join") {
        //     return new JoinNode(params);
    } else if (params.title.toLowerCase() === "add column") {
        return new AddColumnNode(params);
        // } else if (params.title.toLowerCase() === "table") {
        //     return new TableNode(params);
    } else {
        return new LoadNode(params);
    }
}

export abstract class Node {
    id: string = $state("");
    title: string = $state("");
    nodeType: string = $state("");
    prevNodeId: string = $state("");
    columnsOnNodeInput: Column[] = $state([]);
    columnsOnNodeOutput: Column[] = $state([]);
    active: boolean = $state(true);
    invalidState: InvalidState = $state({ active: false, error_msg: "" });

    constructor(params: any) {
        this.id = params.id ? params.id : "node-" + uuidv4();
        this.title = params.title;
        this.prevNodeId = params.prevNodeId;
        this.columnsOnNodeInput = params.columnsOnNodeInput;
        this.columnsOnNodeOutput = params.columnsOnNodeOutput ? params.columnsOnNodeOutput : params.columnsOnNodeInput;
        this.active = params.active ? params.active : true;
        this.invalidState = params.invalidState ? params.invalidState : { active: false, error_msg: "" };
    }

    public abstract submit(params: any): Promise<SparkTransform[]>;
    public abstract setUserInput(params: any): void;
}

export class LoadNode extends Node {
    userInput: ICsvMetadata | IJsonMetadata | IParquetMetadata = $state({ kind: "parquet", path: "" });

    constructor(params: any) {
        super(params);

        this.id = MASTER_NODE_ID;
        this.nodeType = "input";
        this.userInput = params.userInput ? params.userInput : { kind: "parquet", path: "" };
    }
    setUserInput(params: any): void {
        this.userInput = {
            kind: params.inputType,
            ...params.userInput,
        };
    }

    async submit(params: any): Promise<SparkTransform[]> {
        let inputType = params.kind;
        let sessionId = params.session_id;
        delete params.kind;
        delete params.session_id;
        let body = { session_id: sessionId, [inputType]: params };

        const response = await post("rpc/sessionNode/transform/submitLoadDatasetNode", body);
        const transform: SparkTransform = await response.json();

        this.columnsOnNodeOutput = transform.columns;

        return [transform];
    }
}

export class AddColumnNode extends Node {
    expressions: any[];

    constructor(params: any) {
        super(params);
        this.nodeType = "transform";
        this.expressions = [];
    }

    setUserInput(params: any): void {
        this.expressions = params;
    }

    async submit(params: any): Promise<SparkTransform[]> {
        const streamingResponse = await post("rpc/sessionNode/transform/submitNewColumnNode", params);

        const objs = await textBufferSparkStreamingApi(streamingResponse);
        const transforms: SparkTransform[] = JSON.parse(objs);

        return transforms.filter((t) => t.node_id);
    }
}

// class FilterNode extends Node {
//     constructor(title: string, colsInDf: Column[]) {
//         super(title, colsInDf);
//         this.nodeType = "sql";
//     }

//     getClassSnapshot(): NodeSnapshot | any {}

//     getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
//         return {};
//     }

//     setNodeParams(params: any): void {}

//     async submit(params: any): Promise<boolean> {
//         return true;
//     }

//     async submitTransform(params: any): Promise<SparkTransformResponse> {
//         let transformResponse = fetchSparkApi("/filter", {
//             session_id: params.analysisId,
//             node_id: params.nodeId,
//             prev_node_id: params.prevNodeId,
//         });
//         return transformResponse;
//     }

//     parseTransformResponse(res: SparkTransformResponse, params?: any) {}

//     isInvalid(force: boolean, prevNode?: Node): boolean {
//         if (force) {
//             this.setInvalidState(true, "invalid schema");
//             return true;
//         }
//         return false;
//     }
// }

// class JoinNode extends Node {
//     constructor(title: string, colsInDf: Column[]) {
//         super(title, colsInDf);
//         this.nodeType = "sql";
//     }

//     getClassSnapshot(): NodeSnapshot | any {}

//     getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
//         return {};
//     }

//     setNodeParams(params: any): void {}

//     async submit(params: any): Promise<boolean> {
//         return true;
//     }

//     async submitTransform(params: any): Promise<SparkTransformResponse> {
//         let transformResponse = fetchSparkApi("/join", {
//             session_id: params.analysisId,
//             node_id: params.nodeId,
//             prev_node_id: params.prevNodeId,
//         });
//         return transformResponse;
//     }

//     parseTransformResponse(res: SparkTransformResponse, params?: any) {}

//     isInvalid(force: boolean, prevNode?: Node): boolean {
//         if (force) {
//             this.setInvalidState(true, "invalid schema");
//             return true;
//         }
//         return false;
//     }
// }

// class TableNode extends Node {
//     constructor(title: string, colsInDf: Column[]) {
//         super(title, colsInDf);
//         this.nodeType = "visualization";
//     }

//     getClassSnapshot(): NodeSnapshot | any {}

//     getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
//         return {};
//     }

//     setNodeParams(params: any): void {}

//     async submit(params: any): Promise<boolean> {
//         return true;
//     }

//     async submitTransform(params: any): Promise<SparkTransformResponse> {
//         let transformResponse = fetchSparkApi("/table", {
//             session_id: params.analysisId,
//             node_id: params.nodeId,
//             prev_node_id: params.prevNodeId,
//         });
//         return transformResponse;
//     }

//     parseTransformResponse(res: SparkTransformResponse, params?: any) {}

//     isInvalid(force: boolean, prevNode?: Node): boolean {
//         if (force) {
//             this.setInvalidState(true, "invalid schema");
//             return true;
//         }
//         return false;
//     }
// }
