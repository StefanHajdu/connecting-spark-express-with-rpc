import { analysesMock } from "$lib/analyses";
import { STORAGE_KEY_ANALYSES, fromLocalStorage } from "$lib/localStorageHandles";
import { type AnalysesMock } from "$lib/analyses";

export function load(): AnalysesMock {
    let analysesInLS = fromLocalStorage(STORAGE_KEY_ANALYSES);
    return analysesInLS ? analysesInLS : analysesMock;
}
