import { v4 as uuidv4 } from "uuid";
import type { Column, SparkTransform, InvalidState, ICsvMetadata, IJsonMetadata, IParquetMetadata } from "$lib/dtype";
import { post, textBufferSparkStreamingApi } from "$lib/clientApi";
import { AddColumnExpression } from "../Expression/Expression.svelte";

const MASTER_NODE_ID = "0000-0000-0000";

export function nodeFactory(params: any): Node {
  if (params.title === "LoadNode") {
    return new LoadNode(params);
  } else if (params.title === "FilterNode") {
    return new FilterNode(params);
  } else if (params.title === "JoinNode") {
    return new JoinNode(params);
  } else if (params.title === "AddColumnNode") {
    return new AddColumnNode(params);
  } else if (params.title === "TableNode") {
    return new TableNode(params);
  } else {
    return new LoadNode(params);
  }
}

export abstract class Node {
  node_id: string = $state("");
  title: string = $state("");
  nodeType: string = $state("");
  prevNodeId: string = $state("");
  columnsOnNodeInput: Column[] = $state([]);
  columnsOnNodeOutput: Column[] = $state([]);
  active: boolean = $state(true);
  invalidState: InvalidState = $state({ active: false, error_msg: "" });

  constructor(params: any) {
    this.node_id = params.node_id ? params.node_id : "node-" + uuidv4();
    this.title = params.title ? params.title : "NODE TITLE";
    this.prevNodeId = params.prevNodeId;
    this.columnsOnNodeInput = params.columnsOnNodeInput;
    this.columnsOnNodeOutput = params.columnsOnNodeOutput ? params.columnsOnNodeOutput : params.columnsOnNodeInput;
    this.active = params.active !== undefined ? params.active : true;
    this.invalidState = params.invalidState ? params.invalidState : { active: false, error_msg: "" };
  }

  public abstract submit(params: any): Promise<SparkTransform[]>;
  public abstract setUserInput(params: any): void;
  public abstract getUserInput(): any;
}

export class LoadNode extends Node {
  userInput: ICsvMetadata | IJsonMetadata | IParquetMetadata = $state({ kind: "parquet", path: "" });

  constructor(params: any) {
    super(params);

    this.node_id = MASTER_NODE_ID;
    this.nodeType = "input";
    this.userInput = params.userInput ? params.userInput : { kind: "parquet", path: "" };
  }
  setUserInput(userInput: any): void {
    this.userInput = userInput;
  }

  getUserInput(): ICsvMetadata | IJsonMetadata | IParquetMetadata {
    return this.userInput;
  }

  async submit(params: any): Promise<SparkTransform[]> {
    let user_input = this.getUserInput();
    let body = { ...params, [user_input.kind]: user_input };

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

  setUserInput(expressions: any): void {
    if (expressions instanceof Array && expressions.length > 0 && expressions[0] instanceof AddColumnExpression) {
      this.userInput = expressions;
    } else {
      this.userInput = expressions.map((e: any) => {
        // params are optional, some expression don't require them e.g. current_date()
        const params = e.expression.params
          ? e.expression.params.map((param: any) => {
            return {
              name: param.name,
              dtype: param.dtype,
              valueField: JSON.parse(param.valueJson),
            };
          })
          : [];
        return new AddColumnExpression({ ...e.expression, params: params, newColumnName: e.newColumnName });
      });
    }
  }

  getUserInput(): AddColumnExpression[] {
    return this.userInput;
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
  userInput: any;

  constructor(params: any) {
    super(params);
    this.nodeType = "sql";
  }

  setUserInput(params: any): void { }

  getUserInput(): any[] {
    return this.userInput;
  }

  async submit(params: any): Promise<SparkTransform[]> {
    return [];
  }
}

class JoinNode extends Node {
  userInput: any;

  constructor(params: any) {
    super(params);
    this.nodeType = "sql";
  }

  setUserInput(params: any): void { }

  getUserInput(): any[] {
    return this.userInput;
  }

  async submit(params: any): Promise<SparkTransform[]> {
    return [];
  }
}

class TableNode extends Node {
  userInput: any;

  constructor(params: any) {
    super(params);
    this.nodeType = "sql";
  }

  setUserInput(params: any): void { }

  getUserInput(): any[] {
    return this.userInput;
  }

  async submit(params: any): Promise<SparkTransform[]> {
    return [];
  }
}
