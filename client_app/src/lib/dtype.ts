type Param = {
  name: string;
  desc: string;
  value: string | number;
  ptype: string;
};

export type Expression = {
  fname: string;
  params: Param[];
  rename: string;
};

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
