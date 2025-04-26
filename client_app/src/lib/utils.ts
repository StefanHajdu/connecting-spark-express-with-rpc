import { v4 as uuidv4 } from "uuid";

export function getUniqueAnalysesId(): string {
  return "analysis-" + uuidv4();
}

export function sleepNow(delay: number) {
  new Promise((resolve) => setTimeout(resolve, delay * 1000));
}

export function concatMap(map: Map<string, any>): string {
  return map.values().reduce((acc, item) => acc + String(item));
}
