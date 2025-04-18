const BASE_URL = "http://localhost:4444";

async function post(url: URL, body: Object): Promise<any> {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  console.log(response);
  if (!response.ok) {
    throw new Error(`Response status: ${response.status}`);
  }
  return await response.json();
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
  const responseJSON = await post(url, { id: sessionId, name: sessionName });
  return {
    session_id: responseJSON.session_id,
    msg: responseJSON.msg,
  };
}
