const BASE_URL = "http://localhost:4444";

export async function fetchSparkApi(transformRoute: string, body: any): Promise<any> {
  let url = new URL(transformRoute, BASE_URL);
  const response = await post(url, body);
  return response.json();
}

export async function fetchSparkStreamingApi(transformRoute: string, body: any): Promise<Response> {
  let url = new URL(transformRoute, BASE_URL);
  const response = fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return response;
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
