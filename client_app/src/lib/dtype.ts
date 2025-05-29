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

export type SparkLoadFileResponse = {
  transformResponse: SparkTransformResponse;
  size: number;
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
