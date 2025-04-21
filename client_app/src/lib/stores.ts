import { writable, type Writable, get } from "svelte/store";
import { type Column } from "./clientApi";

const empty: Column[] = [];

type ActionState = {
  analysiId: string;
  columns: Column[];
  hidden: boolean;
  inProgress: boolean;
  currAnalysisSeed: number;
  prevAnalysisSeed: number;
  currNode: string;
  prevNode: string;
};

export const actionState = writable({
  // Preview Protocol:
  // 1. Node event "Preview" triggered
  //    - IF previewState.inProgress
  //      OR IF Analysis random seed and Node is not changed
  //      THEN
  //        - ignore event
  //        - disable hidden flag
  // 2. Node sets previewState to:
  //    - current node's id
  //    - current analysis's id
  //    - disable hidden flag
  //    - set previewState.inProgress to true
  // 3. Once preview resolves in DataFrameTable component
  //    - set previewState.inProgress to false
  //    - set currNode to prevNode
  //    - set currPlan to prevPlan
  analysiId: "",
  columns: empty,
  hidden: true,
  inProgress: false,
  currAnalysisSeed: 0,
  prevAnalysisSeed: -1,
  currNode: "0",
  prevNode: "-1",
});

export function requestAction(
  actionState: Writable<ActionState>,
  analysiId: string,
  analysisRandomSeed: number,
  columnHeader: Column[],
  nodeId: string,
): void {
  let localActionState = get(actionState);
  if (
    !(
      localActionState.inProgress ||
      (localActionState.currAnalysisSeed ===
        localActionState.prevAnalysisSeed &&
        localActionState.currNode === localActionState.prevNode)
    )
  ) {
    actionState.update((actionState) => {
      return {
        ...actionState,
        hidden: false,
        inProgress: true,
        analysiId: analysiId,
        columns: columnHeader,
        currAnalysisSeed: analysisRandomSeed,
        currNode: nodeId,
      };
    });
  }
}

export function finishAction(actionState: Writable<ActionState>) {
  let localActionState = get(actionState);
  actionState.update((actionState) => {
    return {
      ...actionState,
      inProgress: false,
      prevAnalysisSeed: localActionState.currAnalysisSeed,
      prevNode: localActionState.currNode,
    };
  });
}
