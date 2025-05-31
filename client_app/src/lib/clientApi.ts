const BASE_URL = "http://localhost:4444";

export async function fetchSparkApi(transformRoute: string, body: any): Promise<any> {
  const response = await post(transformRoute, body);
  return response.json();
}

export async function bufferSparkStreamingApi(streamingResponse: Response): Promise<string> {
  const reader = streamingResponse.body?.getReader();
  let decoder = new TextDecoder();
  let jsonText = "";

  while (true) {
    let chunk = await reader?.read();
    if (chunk?.done) {
      return jsonText;
    }
    jsonText += decoder.decode(chunk?.value, { stream: true });
  }
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
