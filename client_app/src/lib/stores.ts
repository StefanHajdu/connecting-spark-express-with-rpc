import { writable } from "svelte/store";

export const previewState = writable({
  previewHidden: true,
  previewInProgress: false,
});
