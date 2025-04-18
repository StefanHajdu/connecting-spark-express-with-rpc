import { v4 as uuidv4 } from "uuid";

export function getUniqueAnalysesId(): string {
  return "analysis-" + uuidv4();
}
