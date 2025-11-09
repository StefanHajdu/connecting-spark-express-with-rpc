const BASE_URL = "http://localhost:4444";

export async function fetchSparkApi(transformRoute: string, body: any): Promise<any> {
  const response = await post(transformRoute, body);
  return response.json();
}

export async function post(transformRoute: string, body: Object): Promise<Response> {
  let url = new URL(transformRoute, BASE_URL);
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

export async function get(transformRoute: string): Promise<Response> {
  let url = new URL(transformRoute, BASE_URL);
  const response = await fetch(url, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Response status: ${response.status}`);
  }
  return response;
}

export async function readStreamBody(streamingResponse: Response): Promise<string> {
  const reader = streamingResponse.body?.getReader();
  if (!reader) {
    return "";
  }
  let decoder = new TextDecoder();
  let jsonText = "";

  while (true) {
    let chunk = await reader.read();
    if (chunk?.done) {
      return jsonText + decoder.decode();
    }
    jsonText += decoder.decode(chunk.value, { stream: true });
  }
}

export async function jsonStreamSparkStreamingApi<T>(streamingResponse: Response): Promise<T[]> {
  const payload = await readStreamBody(streamingResponse);
  const trimmed = payload.trim();

  if (!trimmed) {
    return [];
  }

  return trimmed.split("\n").map((line) => JSON.parse(line) as T);
}
