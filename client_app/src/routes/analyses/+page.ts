import type { Analysis } from "$lib/dtype";
import { fromLocalStorage, LS_KEY_ANALYSES } from "$lib/localStorageHandles";

export function load(): { analysesRaw: Analysis[] } {
    return { analysesRaw: fromLocalStorage(LS_KEY_ANALYSES) };
}
