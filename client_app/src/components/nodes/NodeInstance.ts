import { v4 as uuidv4 } from "uuid";
import { type Column } from "$lib/dtype";

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
  uuid: string;
  title: string;
  nodeType: string;
  colsAdded: string[];
  colsUsed: Set<string | undefined>;
  colsInDf: Column[];

  constructor(title: string, colsInDf: Column[]) {
    this.uuid = "node-" + uuidv4();
    this.title = title;
    this.colsAdded = [];
    this.colsUsed = new Set([]);
    this.colsInDf = colsInDf;
    this.nodeType = "";
  }
}

class LoadNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.uuid = MASTER_NODE_ID;
    this.nodeType = "load";
  }
}

class AddColumnNode extends Node {
  constructor(title: string, colsInDf: Column[]) {
    super(title, colsInDf);
    this.nodeType = "sql";
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
