import { writable } from "svelte/store";
import type { DataFrame } from "./dtype";

let empty: DataFrame = { columns: [], data: [[]] };

export const lastDataframe = writable(empty);
