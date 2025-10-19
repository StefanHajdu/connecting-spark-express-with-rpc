import { Node } from "../components/Nodes/NodeClass.svelte";

export function sleepNow(delay: number) {
  new Promise((resolve) => setTimeout(resolve, delay * 1000));
}

export function concatMap(map: Map<string, any>): string {
  return map.values().reduce((acc, item) => acc + String(item));
}

export function getIndexOfActivePrevNode(nodesInAnalysis: Node[], nodeIndex: number): number {
  let index = 0;
  for (let i = nodeIndex - 1; i >= 0; i--) {
    if (nodesInAnalysis[i].active) {
      index = i;
      break;
    }
  }
  return index;
}

// export function compileExprObj(expr: Expression): { expression: string; col_name: string } {
//     const params = compileExpr(expr);
//     return { expression: `${expr.fname}(${params.join(", ")})`, col_name: expr.newColumnName };
// }
