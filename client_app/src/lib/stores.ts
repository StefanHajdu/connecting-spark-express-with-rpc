import { writable } from "svelte/store";
import { type Column } from "./clientApi";

const empty: Column[] = [];

export const previewState = writable({
  analysiId: "",
  nodeId: "",
  columns: empty,
  previewHidden: true,
  previewInProgress: false,
});
