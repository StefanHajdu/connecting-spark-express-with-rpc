import { v4 as uuidv4 } from "uuid";
import { type Column } from "$lib/dtype";
import { type SparkTransformResponse } from "$lib/dtype";
import { fetchSparkApi } from "$lib/clientApi";

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
}

class LoadNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.uuid = MASTER_NODE_ID;
    this.nodeType = "load";
  }
}

export class AddColumnNode extends Node {
  expressions: any[];

  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.nodeType = "sql";
    this.expressions = [];
  }

  public async submitTransform(
    analysisId: string,
    nodeId: string,
    prevNodeId: string,
  ): Promise<SparkTransformResponse> {
    let transformResponse = fetchSparkApi("submitNode/NewColumnNode", {
      session_id: analysisId,
      node_id: nodeId,
      prev_node_id: prevNodeId,
      expressions: this.expressions,
    });
    return transformResponse;
  }
}

class FilterNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.nodeType = "sql";
  }
}

class JoinNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.nodeType = "sql";
  }
}

class TableNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.nodeType = "visualization";
  }
}
