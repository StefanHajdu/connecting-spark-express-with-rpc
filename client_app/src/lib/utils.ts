import { v4 as uuidv4 } from "uuid";
import { Node } from "../components/nodes/NodeInstance.svelte";
import { type Expression, type Column } from "./dtype";

export function getUniqueAnalysesId(): string {
  return "analysis-" + uuidv4();
}

export function sleepNow(delay: number) {
  new Promise((resolve) => setTimeout(resolve, delay * 1000));
}

export function concatMap(map: Map<string, any>): string {
  return map.values().reduce((acc, item) => acc + String(item));
}

export function getActivePredecessor(nodesInAnalysis: Node[], nodeIndex: number): number {
  let index = 0;
  for (let i = nodeIndex - 1; i >= 0; i--) {
    if (nodesInAnalysis[i].active) {
      index = i;
      break;
    }
  }
  return index;
}

export function compileExpr(expr: Expression): string[] {
  let params: string[] = [];
  for (let param of expr.params) {
    if (param.ptype === "single_col") {
      if (param.valueField.source === "input" && typeof param.valueField.value === "string") {
        params.push(`'${param.valueField.value}'`);
      } else {
        params.push(`${param.valueField.value}`);
      }
    } else if (param.ptype === "multi_col") {
      params.push(`${param.valueField.value}`);
    } else if (param.ptype === "text") {
      params.push(`'${param.valueField.value}'`);
    } else if (param.ptype === "number") {
      params.push(`${param.valueField.value}`);
    }
  }
  return params;
}

export function compileExprString(expr: Expression): string {
  const params = compileExpr(expr);
  return `${expr.fname}(${params.join(", ")}) as ${expr.newColumnName}`;
}

export function compileExprObj(expr: Expression): { expression: string; col_name: string } {
  const params = compileExpr(expr);
  return { expression: `${expr.fname}(${params.join(", ")})`, col_name: expr.newColumnName };
}

export function syncNodeColsOnAdd(nodesInAnalysis: Node[], nodeIndex: number): void {
  let colsAdded = nodesInAnalysis[nodeIndex].colsInNode.filter((col: Column) =>
    nodesInAnalysis[nodeIndex].colsAdded.has(col.name),
  );
  for (let i = nodeIndex + 1; i < nodesInAnalysis.length; i++) {
    let colsInTransformSnapshot = nodesInAnalysis[i].colsInTransform;
    nodesInAnalysis[i].colsInNode = [...colsInTransformSnapshot, ...colsAdded];
  }
}

export function syncNodeColsOnRemove(nodesInAnalysis: Node[], nodeIndex: number): void {
  let colsToRemove = nodesInAnalysis[nodeIndex].colsAdded;
  if (colsToRemove.size > 0) {
    for (let i = nodeIndex + 1; i < nodesInAnalysis.length; i++) {
      let colsReduced = nodesInAnalysis[i].colsInNode.filter((col: Column) => !colsToRemove.has(col.name));
      nodesInAnalysis[i].colsInNode = colsReduced;
    }
  }
}
