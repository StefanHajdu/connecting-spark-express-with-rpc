import { v4 as uuidv4 } from "uuid";
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

export function compileExpr(expr: Expression, colsInDf: Column[]): string {
  let params = [];

  for (let param of expr.params) {
    if (param.ptype === "single_col") {
      if (
        colsInDf.findIndex((i: Column) => {
          return i.name === param.value;
        }) < 0
      ) {
        if (typeof param.value === "string") {
          params.push(`lit('${param.value}')`);
        } else {
          params.push(`lit(${param.value})`);
        }
      } else {
        params.push(param.value);
      }
    } else if (param.ptype === "multi_col") {
      params.push(param.value);
    } else if (param.ptype === "text") {
      params.push(`'${param.value}'`);
    } else if (param.ptype === "number") {
      params.push(param.value);
    }
  }

  return `${expr.fname}(${params.join(", ")}) as ${expr.rename}`;
}
