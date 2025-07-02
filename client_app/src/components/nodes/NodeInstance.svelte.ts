import { v4 as uuidv4 } from "uuid";
import type { Column, SparkTransformResponse, Expression, Param } from "$lib/dtype";
import { fetchSparkApi } from "$lib/clientApi";
import { compileExprObj } from "$lib/utils";

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
    colsAdded: Set<string> = $state(new Set([]));
    colsUsed: Set<string | undefined> = $state(new Set([]));
    colsInNode: Column[] = $state([]);
    colsInTransform: Column[] = $state([]);
    active: boolean = $state(true);

    constructor(title: string, cols: Column[]) {
        this.uuid = "node-" + uuidv4();
        this.title = title;
        this.colsInNode = cols;
        this.colsInTransform = cols;
    }

    abstract submitTransform(params: any): Promise<SparkTransformResponse>;
    abstract processTransformResponse(res: SparkTransformResponse, params?: any): void;
}

class LoadNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.uuid = MASTER_NODE_ID;
        this.nodeType = "load";
    }

    public async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitLoadDatasetNode", params.body);
        return transformResponse;
    }

    processTransformResponse(res: SparkTransformResponse, params?: any) {
        this.colsInTransform = this.colsInNode = res.columns;
        this.colsAdded = new Set(res.columns.map((col: Column) => col.name));
    }
}

export class AddColumnNode extends Node {
    expressions: any[];

    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
        this.expressions = [];
    }

    public async submitTransform(params: any): Promise<SparkTransformResponse> {
        console.log(params);
        let transformResponse = fetchSparkApi("rpc/sessionNode/transform/submitNewColumnNode", {
            ...params,
            expressions: params.expressions.map((expr: any) => compileExprObj(expr)),
        });
        return transformResponse;
    }

    processTransformResponse(res: SparkTransformResponse, params?: any) {
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
}

class FilterNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
    }

    public async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/filter", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    processTransformResponse(res: SparkTransformResponse, params?: any) {}
}

class JoinNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "sql";
    }

    public async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/join", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    processTransformResponse(res: SparkTransformResponse, params?: any) {}
}

class TableNode extends Node {
    constructor(title: string, colsInDf: Column[]) {
        super(title, colsInDf);
        this.nodeType = "visualization";
    }

    public async submitTransform(params: any): Promise<SparkTransformResponse> {
        let transformResponse = fetchSparkApi("/table", {
            session_id: params.analysisId,
            node_id: params.nodeId,
            prev_node_id: params.prevNodeId,
        });
        return transformResponse;
    }

    processTransformResponse(res: SparkTransformResponse, params?: any) {}
}
