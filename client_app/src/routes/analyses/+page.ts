import type { IAnalysis } from "$lib/dtype";
import { fromLocalStorage, LS_KEY_ANALYSES } from "$lib/localStorageHandles";

export function load(): { analysesRaw: IAnalysis[] } {
    return { analysesRaw: fromLocalStorage(LS_KEY_ANALYSES) };
}
