import type { ICsvMetadata, IJsonMetadata, IParquetMetadata } from "$lib/dtype";

export class CsvMetadata implements ICsvMetadata {
    path: string;
    delimiter: string;
    includeHeader: string;

    constructor(path: string, delimiter: string, includeHeader: boolean) {
        this.path = path;
        this.delimiter = delimiter;
        this.includeHeader = includeHeader ? "yes" : "no";
    }
}

export class JsonMetadata implements IJsonMetadata {
    path: string;
    multiline: string;

    constructor(path: string, multiline: boolean) {
        this.path = path;
        this.multiline = multiline ? "yes" : "no";
    }
}

export class ParquetMetadata implements IParquetMetadata {
    path: string;

    constructor(path: string) {
        this.path = path;
    }
}
