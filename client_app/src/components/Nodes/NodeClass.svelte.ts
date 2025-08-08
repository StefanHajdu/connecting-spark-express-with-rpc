import { v4 as uuidv4 } from "uuid";
import type {
    Column,
    SparkTransformResponse,
    Expression,
    Param,
    InvalidState,
    NodeSnapshot,
    ICsvMetadata,
    IJsonMetadata,
    IParquetMetadata,
    LoadNodeSnapshot,
} from "$lib/dtype";
import { post, textBufferSparkStreamingApi, fetchSparkApi } from "$lib/clientApi";
// import { compileExprObj, syncInNewColumns, getActivePredecessor } from "$lib/utils";
import { compileExprObj } from "$lib/utils";

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

    public setInvalidState(value: boolean, description: string) {
        this.invalidState = { active: value, error_msg: description };
    }

    public getSnapshot(): NodeSnapshot {
        return {
            uuid: $state.snapshot(this.id),
            title: $state.snapshot(this.title),
            nodeType: $state.snapshot(this.nodeType),
            prevNodeId: $state.snapshot(this.prevNodeId),
            columnsOnNodeInput: $state.snapshot(this.columnsOnNodeInput),
            columnsOnNodeOutput: $state.snapshot(this.columnsOnNodeOutput),
            active: $state.snapshot(this.active),
            invalidState: $state.snapshot(this.invalidState),
        };
    }

    public abstract submit(params: any): Promise<boolean>;
    public abstract setUserInput(params: any): void;
    public abstract fetchTransform(params: any): Promise<SparkTransformResponse>;
    public abstract isInvalid(force: boolean, prevNode?: Node): boolean;
    public abstract getNodeSnapshot(): NodeSnapshot | any;
}

export class LoadNode extends Node {
    userInput: ICsvMetadata | IJsonMetadata | IParquetMetadata = $state({ kind: "parquet", path: "" });

    constructor(params: any) {
        super(params);

        this.id = MASTER_NODE_ID;
        this.nodeType = "input";
        this.userInput = params.userInput ? params.userInput : { kind: "parquet", path: "" };
    }

    getNodeSnapshot(): LoadNodeSnapshot {
        return {
            ...this.getSnapshot(),
            userInput: this.userInput,
        };
    }

    setUserInput(params: any): void {
        this.userInput = {
            kind: params.inputType,
            ...params.userInput,
        };
    }

    async submit(params: any): Promise<boolean> {
        let transformResponse = await this.fetchTransform(params);

        if (transformResponse) {
            this.columnsOnNodeOutput = transformResponse.columns;
            return true;
        } else {
            return false;
        }
    }

    async fetchTransform(params: any): Promise<SparkTransformResponse> {
        // transform {kind: "csv", session_id: "", path: "", ...} to {session_id: "", csv: {path: "", ...}}
        let inputType = params.kind;
        let sessionId = params.session_id;
        delete params.kind;
        delete params.session_id;
        let body = { session_id: sessionId, [inputType]: params };
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitLoadDatasetNode", body);
        return transformResponse;
    }

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "Invalid state was forced.");
            return true;
        }
        return false;
    }
}

export class AddColumnNode extends Node {
    expressions: any[];

    constructor(params: any) {
        super(params);
        this.nodeType = "transform";
        this.expressions = [];
    }

    getNodeSnapshot(): any {
        return {};
    }

    // getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
    //     return {
    //         analysisId: analysisId,
    //         nodeUuid: nodesInAnalysis[nodeIndex].uuid,
    //         prevNodeUuid: nodesInAnalysis[getActivePredecessor(nodesInAnalysis, nodeIndex)].uuid,
    //         expressions: this.expressions,
    //         nodesInAnalysis: nodesInAnalysis,
    //         nodeIndex: nodeIndex,
    //     };
    // }

    setUserInput(params: any): void {
        this.expressions = params;
    }

    async submit(params: any): Promise<boolean> {
        const streamingResponse = await post("rpc/sessionNode/transform/submitNewColumnNode", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
            expressions: params.expressions,
        });

        const objs = await textBufferSparkStreamingApi(streamingResponse);

        console.log(JSON.parse(objs));

        return true;
    }

    async fetchTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitNewColumnNode", {
            ...params,
            expressions: params.expressions ? params.expressions.map((expr: any) => compileExprObj(expr)) : [],
        });
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {
        // this.colsAdded = new Set(params.expressions.map((expr: Expression) => expr.newColumnName));
        // this.colsUsed = new Set(
        //     params.expressions
        //         .flatMap((expr: Expression) => {
        //             return expr.params
        //                 .filter((param: Param) => {
        //                     return param.valueField.source === "col" || param.valueField.source === "cols";
        //                 })
        //                 .map((param: Param) => {
        //                     if (param.valueField.source === "cols") {
        //                         return typeof param.valueField.value === "string"
        //                             ? param.valueField.value.split(",")
        //                             : undefined;
        //                     } else {
        //                         return typeof param.valueField.value === "string" ? param.valueField.value : undefined;
        //                     }
        //                 });
        //         })
        //         .flat(),
        // );
    }

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "Invalid state was forced.");
            return true;
        }

        // if (prevNode) {
        //     // invalid if node uses columns that are not present in prev node
        //     const diff = this.colsUsed.difference(this.colsToSet(prevNode.colsInNode));
        //     if (diff.size > 0) {
        //         this.invalidState = {
        //             value: true,
        //             description: `Missing or renamed columns: [${[...diff].join(", ")}], please manually fix and submit node`,
        //         };
        //         return true;
        //     }
        // }

        return false;
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
