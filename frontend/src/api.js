import config from "./config.js";

export async function createSession(userId) {
  const res = await fetch(`${config.gatewayUrl}/create_session`, {
    method: "POST",
    body: JSON.stringify({ user_id: userId }),
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    throw new Error(`Gateway error: ${res.status}`);
  }

  return res.json(); // { host, port, token, user_id }
}