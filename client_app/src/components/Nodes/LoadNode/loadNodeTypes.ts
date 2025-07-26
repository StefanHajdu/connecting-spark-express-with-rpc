export class CsvMetadata {
    path: string;
    delimiter: string;
    includeHeader: string;

    constructor(path: string, delimiter: string, includeHeader: boolean) {
        this.path = path;
        this.delimiter = delimiter;
        this.includeHeader = includeHeader ? "yes" : "no";
    }
}

export class JsonMetadata {
    path: string;
    multiline: string;

    constructor(path: string, multiline: boolean) {
        this.path = path;
        this.multiline = multiline ? "yes" : "no";
    }
}

export class ParquetMetadata {
    path: string;

    constructor(path: string) {
        this.path = path;
    }
}
