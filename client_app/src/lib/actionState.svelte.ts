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

export const actionState: ActionState = $state({
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
  analysiId: string,
  analysisRandomSeed: number,
  columnHeader: Column[],
  nodeId: string,
): void {
  if (
    !(
      actionState.inProgress ||
      (actionState.currAnalysisSeed === actionState.prevAnalysisSeed &&
        nodeId === actionState.prevNode)
    )
  ) {
    actionState.hidden = false;
    actionState.inProgress = true;
    actionState.analysiId = analysiId;
    actionState.columns = columnHeader;
    actionState.currAnalysisSeed = analysisRandomSeed;
    actionState.currNode = nodeId;
  }
}

export function finishAction() {
  actionState.inProgress = false;
  actionState.prevAnalysisSeed = actionState.currAnalysisSeed;
  actionState.prevNode = actionState.currNode;
}
