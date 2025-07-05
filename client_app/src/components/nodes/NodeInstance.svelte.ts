import { v4 as uuidv4 } from "uuid";
import type { Column, SparkTransformResponse, Expression, Param, InvalidState } from "$lib/dtype";
import { fetchSparkApi } from "$lib/clientApi";
import { compileExprObj, syncInNewColumns, getActivePredecessor } from "$lib/utils";

const MASTER_NODE_ID = "0000-0000-0000";

export function nodeFactoryMethod(title: string, colsInDf: Column[]): Node {
    if (title.toLowerCase() === "load") {
        return new LoadNode(title, colsInDf);
    } else if (title.toLowerCase() === "filter") {
        return new FilterNode(title, colsInDf);
    } else if (title.toLowerCase() === "join") {
        return new JoinNode(title, colsInDf);
    } else if (title.toLowerCase() === "add column") {
        return new AddColumnNode(title, colsInDf);
    } else if (title.toLowerCase() === "table") {
        return new TableNode(title, colsInDf);
    } else {
        return new LoadNode(title, colsInDf);
    }
}

export abstract class Node {
    uuid: string = $state("");
    title: string = $state("");
    nodeType: string = $state("");
    colsAdded: Set<string> = $state(new Set([])); // column names added by node
    colsUsed: Set<string | undefined> = $state(new Set([])); // column names used by node
    colsInNode: Column[] = $state([]);
    colsInTransform: Column[] = $state([]);
    active: boolean = $state(true);
    invalidState: InvalidState = $state({ value: false, description: "" });

    constructor(title: string, cols: Column[]) {
        this.uuid = "node-" + uuidv4();
        this.title = title;
        this.colsInNode = cols;
        this.colsInTransform = cols;
    }

    public setInvalidState(value: boolean, description: string) {
        this.invalidState = { value: value, description: description };
    }

    public colsToSet(cols: Column[]): Set<string> {
        return new Set(cols.map((col) => col.name));
    }

    public abstract submit(params: any): Promise<boolean>;
    public abstract getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any;
    public abstract submitTransform(params: any): Promise<SparkTransformResponse>;
    public abstract parseTransformResponse(res: SparkTransformResponse, params?: any): void;
    public abstract isInvalid(force: boolean, prevNode?: Node): boolean;
}

class LoadNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.uuid = MASTER_NODE_ID;
        this.nodeType = "load";
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {};
    }

    async submit(params: any): Promise<boolean> {
        let transformRes = await this.submitTransform(params);

        if (transformRes) {
            this.parseTransformResponse(transformRes);
            return true;
        } else {
            return false;
        }
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitLoadDatasetNode", params);
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

export class AddColumnNode extends Node {
    expressions: any[];

    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
        this.expressions = [];
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {
            analysisId: analysisId,
            nodeUuid: nodesInAnalysis[nodeIndex].uuid,
            prevNodeUuid: nodesInAnalysis[getActivePredecessor(nodesInAnalysis, nodeIndex)].uuid,
            expressions: this.expressions,
            nodesInAnalysis: nodesInAnalysis,
            nodeIndex: nodeIndex,
        };
    }

    async submit(params: any): Promise<boolean> {
        let transformRes: SparkTransformResponse = await this.submitTransform({
            session_id: params.analysisId,
            node_id: params.nodeUuid,
            prev_node_id: params.prevNodeUuid,
            expressions: params.expressions,
        });
        if (transformRes) {
            this.parseTransformResponse(transformRes, { expressions: params.expressions });
            syncInNewColumns(params.nodesInAnalysis, params.nodeIndex);
            return true;
        } else {
            return false;
        }
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitNewColumnNode", {
            ...params,
            expressions: params.expressions.map((expr: any) => compileExprObj(expr)),
        });
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {
        this.colsInTransform = this.colsInNode = res.columns;
        this.colsAdded = new Set(params.expressions.map((expr: Expression) => expr.newColumnName));
        this.colsUsed = new Set(
            params.expressions
                .flatMap((expr: Expression) => {
                    return expr.params
                        .filter((param: Param) => {
                            return param.valueField.source === "col" || param.valueField.source === "cols";
                        })
                        .map((param: Param) => {
                            if (param.valueField.source === "cols") {
                                return typeof param.valueField.value === "string"
                                    ? param.valueField.value.split(",")
                                    : undefined;
                            } else {
                                return typeof param.valueField.value === "string" ? param.valueField.value : undefined;
                            }
                        });
                })
                .flat(),
        );
        this.expressions = params.expressions;
    }

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "Invalid schema upstream");
            return true;
        }

        if (prevNode) {
            // invalid if node uses columns that are not present in prev node
            const diff = this.colsUsed.difference(this.colsToSet(prevNode.colsInNode));
            if (diff.size > 0) {
                this.invalidState = {
                    value: true,
                    description: `Missing or renamed columns: ${[...diff].join(", ")}, please manually fix and submit node`,
                };
                return true;
            }
        }

        return false;
    }
}

class FilterNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {};
    }

    async submit(params: any): Promise<boolean> {
        return true;
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/filter", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {}

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "invalid schema");
            return true;
        }
        return false;
    }
}

class JoinNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {};
    }

    async submit(params: any): Promise<boolean> {
        return true;
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/join", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {}

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "invalid schema");
            return true;
        }
        return false;
    }
}

class TableNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "visualization";
    }

    getSubmitParams(analysisId: string, nodesInAnalysis: Node[], nodeIndex: number): any {
        return {};
    }

    async submit(params: any): Promise<boolean> {
        return true;
    }

    async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/table", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    parseTransformResponse(res: SparkTransformResponse, params?: any) {}

    isInvalid(force: boolean, prevNode?: Node): boolean {
        if (force) {
            this.setInvalidState(true, "invalid schema");
            return true;
        }
        return false;
    }
}
