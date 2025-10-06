import { Node } from "../components/Nodes/NodeClass.svelte.js";

export interface IAnalysis {
    id: string;
    name: string;
    status: string;
    buildTime: string;
    resources: string;
    rest: string;
    selected: boolean;
    nodes: Node[];
}

export interface InvalidState {
    active: boolean;
    error_msg: string;
}

export type SparkActionlResponse = {
    session_id: string;
    msg: string;
    columns: string;
    schema: string;
    count: number;
};

export type CreateSessionResponse = {
    session_id: string;
    msg: string;
};

export type Column = {
    name: string;
    dtype: string;
};

export type PreviewColumn = {
    name: string;
    type: string;
};

export type SparkTransform = {
    session_id: string;
    node_id: string;
    columns: Column[];
    invalid_state: InvalidState;
    active: boolean;
    prev_node_id: string;
    title: string;
    user_input: string;
};

type ValueType = "col" | "input" | "cols";
type CustomInputType = "number" | "text";

interface ValueField {
    value: string | number;
    source: ValueType;
}

export interface Param {
    desc: string;
    name: string;
    ptype: string;
    valueField: ValueField;
}

export interface Expression {
    uuid: string;
    fname: string;
    params: Param[];
    newColumnName: string;
    sparkTypes: Set<string>;
    customInput: CustomInputType;
}

type SparkColumn = {
    name: string;
    type: string;
};

export type DataFrame = {
    columns: SparkColumn[];
    data: string[][];
};

export interface ICsvMetadata {
    kind: "csv";
    path: string;
    delimiter: string;
    include_header: boolean;
}
export interface IJsonMetadata {
    kind: "json";
    path: string;
    multiline: boolean;
}
export interface IParquetMetadata {
    kind: "parquet";
    path: string;
}

export type ButtonColor =
    | "dark"
    | "blue"
    | "none"
    | "red"
    | "yellow"
    | "green"
    | "purple"
    | "light"
    | "primary"
    | "alternative"
    | undefined;
