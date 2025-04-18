const BASE_URL = "http://localhost:4444";

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

type CreateSessionResponse = {
  session_id: string;
  msg: string;
};

export async function fetchCreateSession(
  sessionId: string,
  sessionName: string,
): Promise<CreateSessionResponse> {
  let url = new URL("createSession", BASE_URL);
  const response = await post(url, { id: sessionId, name: sessionName });
  return response.json();
}

type Column = {
  name: string;
  dtype: string;
};

type SparkTransformResponse = {
  session_id: string;
  msg: string;
  columns: Column[];
};

type SparkLoadFileResponse = {
  transformResponse: SparkTransformResponse;
  size: number;
};

export async function fetchLoadTransform(
  transformRoute: string,
  body: any,
): Promise<SparkLoadFileResponse> {
  let url = new URL(transformRoute, BASE_URL);
  const response = await post(url, body);
  return response.json();
}

export async function fetchTransform(
  transformRoute: string,
  body: any,
): Promise<SparkTransformResponse> {
  let url = new URL(transformRoute, BASE_URL);
  const response = await post(url, body);
  return response.json();
}
