import { browser } from "$app/environment";

export const STORAGE_KEY_ANALYSES = "analyses";

export function fromLocalStorage(storageKey: string) {
    if (browser) {
        const storedValue = window.localStorage.getItem(storageKey);
        if (storedValue !== undefined && storedValue !== null) {
            let storedValueParsed = JSON.parse(storedValue);
            return storedValueParsed;
        }
    }
    return undefined;
}

export function toLocalStorage(storageKey: string, data: any) {
    if (browser) {
        let storageValue = typeof data === "object" ? JSON.stringify(data) : data;
        window.localStorage.setItem(storageKey, storageValue);
    }
}
