export interface Analysis {
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
    value: boolean;
    description: string;
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

export type SparkTransformResponse = {
    session_id: string;
    msg: string;
    columns: Column[];
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
