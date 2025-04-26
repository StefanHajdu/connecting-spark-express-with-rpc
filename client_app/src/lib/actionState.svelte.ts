import { type Column } from "./clientApi";

const empty: Column[] = [];

type ActionState = {
  analysiId: string;
  nodeId: string;
  columns: Column[];
  confirmed: boolean;
  previewTableHidden: boolean;
};

export const actionState: ActionState = $state({
  analysiId: "",
  nodeId: "",
  columns: empty,
  confirmed: false,
  previewTableHidden: true,
});

export function requestAction(
  analysiId: string,
  columns: Column[],
  nodeId: string,
  action: string,
): void {
  actionState.analysiId = analysiId;
  actionState.columns = columns;
  actionState.nodeId = nodeId;
  actionState.confirmed = true;
  if (action === "preview") {
    actionState.previewTableHidden = false;
  }
}

export function finishAction(): void {
  actionState.confirmed = false;
}
