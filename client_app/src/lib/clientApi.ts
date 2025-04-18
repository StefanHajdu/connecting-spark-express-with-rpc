const BASE_URL = "http://localhost:4444";

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

export async function fetchSparkApi(
  transformRoute: string,
  body: any,
): Promise<any> {
  let url = new URL(transformRoute, BASE_URL);
  const response = await post(url, body);
  return response.json();
}

async function post(url: URL, body: Object): Promise<Response> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`Response status: ${response.status}`);
  }
  return response;
}
