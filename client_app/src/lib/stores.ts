import { writable } from "svelte/store";

let empty: any[] = [];

export const lastPreviewedRows = writable(empty);
