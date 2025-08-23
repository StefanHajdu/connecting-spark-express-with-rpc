import { v4 as uuidv4 } from "uuid";
import type { Column, SparkTransform, InvalidState, ICsvMetadata, IJsonMetadata, IParquetMetadata } from "$lib/dtype";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";
import { AddColumnExpression } from "../Expression/Expression.svelte";

const MASTER_NODE_ID = "0000-0000-0000";

export function nodeFactory(params: any): Node {
    if (params.title.toLowerCase() === "load") {
        return new LoadNode(params);
    } else if (params.title.toLowerCase() === "filter") {
        return new FilterNode(params);
    } else if (params.title.toLowerCase() === "join") {
        return new JoinNode(params);
    } else if (params.title.toLowerCase() === "add column") {
        return new AddColumnNode(params);
    } else if (params.title.toLowerCase() === "table") {
        return new TableNode(params);
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

        const streamingResponse = await post("rpc/sessionNode/transform/submitLoadDatasetNode", body);
        const objs = await textBufferSparkStreamingApi(streamingResponse);
        const transforms: SparkTransform[] = JSON.parse(objs);

        this.columnsOnNodeOutput = transforms[0].columns;

        return transforms;
    }
}

export class AddColumnNode extends Node {
    userInput: AddColumnExpression[];

    constructor(params: any) {
        super(params);
        this.nodeType = "transform";
        this.userInput = params.userInput ? params.userInput : [];
    }

    setUserInput(expressions: AddColumnExpression[]): void {
        this.userInput = expressions;
    }

    async submit(params: any): Promise<SparkTransform[]> {
        const body = { ...params, user_input: this.userInput.map((u) => u.pack()) };
        const streamingResponse = await post("rpc/sessionNode/transform/submitAddColumnNode", body);
        const objs = await textBufferSparkStreamingApi(streamingResponse);
        const transforms: SparkTransform[] = JSON.parse(objs);

        return transforms;
    }
}

class FilterNode extends Node {
    constructor(params: any) {
        super(params);
        this.nodeType = "sql";
    }

    setUserInput(params: any): void {}

    async submit(params: any): Promise<SparkTransform[]> {
        return [];
    }
}

class JoinNode extends Node {
    constructor(params: any) {
        super(params);
        this.nodeType = "sql";
    }

    setUserInput(params: any): void {}

    async submit(params: any): Promise<SparkTransform[]> {
        return [];
    }
}

class TableNode extends Node {
    constructor(params: any) {
        super(params);
        this.nodeType = "sql";
    }

    setUserInput(params: any): void {}

    async submit(params: any): Promise<SparkTransform[]> {
        return [];
    }
}
