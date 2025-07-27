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
import { fetchSparkApi } from "$lib/clientApi";
import { compileExprObj, syncInNewColumns, getActivePredecessor } from "$lib/utils";

const MASTER_NODE_ID = "0000-0000-0000";

export function nodeFactory(params: any): Node {
    if (params.title.toLowerCase() === "load") {
        return new LoadNode(params);
        // } else if (params.title.toLowerCase() === "filter") {
        //     return new FilterNode(params);
        // } else if (params.title.toLowerCase() === "join") {
        //     return new JoinNode(params);
        // } else if (params.title.toLowerCase() === "add column") {
        //     return new AddColumnNode(params);
        // } else if (params.title.toLowerCase() === "table") {
        //     return new TableNode(params);
    } else {
        return new LoadNode(params);
    }
}

export abstract class Node {
    uuid: string = $state("");
    title: string = $state("");
    nodeType: string = $state("");
    colsAdded: Set<string> = $state(new Set([])); // column names added by node
    colsUsed: Set<string> = $state(new Set([])); // column names used by node
    colsInNode: Column[] = $state([]);
    colsInTransform: Column[] = $state([]);
    active: boolean = $state(true);
    invalidState: InvalidState = $state({ value: false, description: "" });
    submitted: boolean = $state(false);

    constructor(params: any) {
        this.title = params.title;
        this.colsInNode = params.colsInNode;
        this.colsInTransform = params.colsInTransform ? params.colsInTransform : params.colsInNode;
        this.uuid = params.uuid ? params.uuid : "node-" + uuidv4();
        this.nodeType = params.nodeType ? params.nodeType : "";
        this.colsAdded = params.colsAdded ? new Set(params.colsAdded) : new Set([]);
        this.colsUsed = params.colsUsed ? new Set(params.colsUsed) : new Set([]);
        this.active = params.active ? params.active : true;
        this.invalidState = params.invalidState ? params.invalidState : { value: false, description: "" };
        this.submitted = params.submitted ? params.submitted : false;
    }

    public setInvalidState(value: boolean, description: string) {
        this.invalidState = { value: value, description: description };
    }

    public colsToSet(cols: Column[]): Set<string> {
        return new Set(cols.map((col) => col.name));
    }

    public getSnapshot(): NodeSnapshot {
        return {
            uuid: $state.snapshot(this.uuid),
            title: $state.snapshot(this.title),
            nodeType: $state.snapshot(this.nodeType),
            colsAdded: $state.snapshot(Array.from(this.colsAdded)),
            colsUsed: $state.snapshot(Array.from(this.colsUsed)),
            colsInNode: $state.snapshot(this.colsInNode),
            colsInTransform: $state.snapshot(this.colsInTransform),
            active: $state.snapshot(this.active),
            invalidState: $state.snapshot(this.invalidState),
            submitted: $state.snapshot(this.submitted),
        };
    }

    public abstract setUserInput(params: any): void;
    public abstract submit(params: any): Promise<boolean>;
    public abstract getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any;
    public abstract submitTransform(params: any): Promise<SparkTransformResponse>;
    public abstract parseTransformResponse(res: SparkTransformResponse, params?: any): void;
    public abstract isInvalid(force: boolean, prevNode?: Node): boolean;
    public abstract getClassSnapshot(): NodeSnapshot | any;
}

export class LoadNode extends Node {
    userInput: ICsvMetadata | IJsonMetadata | IParquetMetadata = $state({ kind: "parquet", path: "" });

    constructor(params: any) {
        super(params);

        this.uuid = MASTER_NODE_ID;
        this.nodeType = "load";
        this.userInput = params.userInput ? params.userInput : { kind: "parquet", path: "" };
    }

    getClassSnapshot(): LoadNodeSnapshot {
        return {
            ...this.getSnapshot(),
            userInput: this.userInput,
        };
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {};
    }

    setUserInput(params: any): void {
        this.userInput = {
            kind: params.inputType,
            ...params.userInput,
        };
    }

    async submit(params: any): Promise<boolean> {
        let transformRes = await this.submitTransform(params);

        if (transformRes) {
            this.parseTransformResponse(transformRes);
            this.submitted = true;
            return true;
        } else {
            this.submitted = false;
            return false;
        }
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        // transform {kind: "csv", session_id: "", path: "", ...} to {session_id: "", csv: {path: "", ...}}, it looks better in request body
        let inputType = params.kind;
        let sessionId = params.session_id;
        delete params.kind;
        delete params.session_id;
        let body = { session_id: sessionId, [inputType]: params };
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitLoadDatasetNode", body);
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {
        this.colsInTransform = this.colsInNode = res.columns;
        this.colsAdded = new Set(res.columns.map((col: Column) => col.name));
    }

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "invalid schema");
            return true;
        }
        return false;
    }
}

// export class AddColumnNode extends Node {
//     expressions: any[];

//     constructor(title: string, colsInDf: Column[]) {
//         super(title, colsInDf);
//         this.nodeType = "sql";
//         this.expressions = [];
//     }

//     getClassSnapshot(): NodeSnapshot | any {}

//     getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
//         return {
//             analysisId: analysisId,
//             nodeUuid: nodesInAnalysis[nodeIndex].uuid,
//             prevNodeUuid: nodesInAnalysis[getActivePredecessor(nodesInAnalysis, nodeIndex)].uuid,
//             expressions: this.expressions,
//             nodesInAnalysis: nodesInAnalysis,
//             nodeIndex: nodeIndex,
//         };
//     }

//     setNodeParams(params: any): void {}

//     async submit(params: any): Promise<boolean> {
//         let transformRes: SparkTransformResponse = await this.submitTransform({
//             session_id: params.analysisId,
//             node_id: params.nodeUuid,
//             prev_node_id: params.prevNodeUuid,
//             expressions: params.expressions,
//         });
//         if (transformRes) {
//             this.parseTransformResponse(transformRes, { expressions: params.expressions });
//             syncInNewColumns(params.nodesInAnalysis, params.nodeIndex);
//             return true;
//         } else {
//             return false;
//         }
//     }

//     async submitTransform(params: any): Promise<SparkTransformResponse> {
//         let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitNewColumnNode", {
//             ...params,
//             expressions: params.expressions.map((expr: any) => compileExprObj(expr)),
//         });
//         return transformResponse;
//     }

//     parseTransformResponse(res: SparkTransformResponse, params?: any) {
//         this.colsInTransform = this.colsInNode = res.columns;
//         this.colsAdded = new Set(params.expressions.map((expr: Expression) => expr.newColumnName));
//         this.colsUsed = new Set(
//             params.expressions
//                 .flatMap((expr: Expression) => {
//                     return expr.params
//                         .filter((param: Param) => {
//                             return param.valueField.source === "col" || param.valueField.source === "cols";
//                         })
//                         .map((param: Param) => {
//                             if (param.valueField.source === "cols") {
//                                 return typeof param.valueField.value === "string"
//                                     ? param.valueField.value.split(",")
//                                     : undefined;
//                             } else {
//                                 return typeof param.valueField.value === "string" ? param.valueField.value : undefined;
//                             }
//                         });
//                 })
//                 .flat(),
//         );
//         this.expressions = params.expressions;
//     }

//     isInvalid(force: boolean, prevNode?: Node): boolean {
//         if (force) {
//             this.setInvalidState(true, "Invalid schema upstream");
//             return true;
//         }

//         if (prevNode) {
//             // invalid if node uses columns that are not present in prev node
//             const diff = this.colsUsed.difference(this.colsToSet(prevNode.colsInNode));
//             if (diff.size > 0) {
//                 this.invalidState = {
//                     value: true,
//                     description: `Missing or renamed columns: [${[...diff].join(", ")}], please manually fix and submit node`,
//                 };
//                 return true;
//             }
//         }

//         return false;
//     }
// }

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
