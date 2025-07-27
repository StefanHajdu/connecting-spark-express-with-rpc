import { browser } from "$app/environment";

export const LS_KEY_ANALYSES = "analyses";
export const LS_KEY_SCOPED = "scoped";

export function fromLocalStorage(storageKey: string): any {
    if (browser) {
        const storedValue = window.localStorage.getItem(storageKey);
        if (storedValue !== undefined && storedValue !== null) {
            let storedValueParsed = JSON.parse(storedValue);
            return storedValueParsed;
        }
    }
    return {};
}

export function toLocalStorage(storageKey: string, data: any): void {
    if (browser) {
        let storageValue = typeof data === "object" ? JSON.stringify(data) : data;
        window.localStorage.setItem(storageKey, storageValue);
    }
}
