import { verifyCredentials } from "@/lib/auth";
import { createSession } from "@/lib/session";

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const username = typeof body?.username === "string" ? body.username : "";
  const password = typeof body?.password === "string" ? body.password : "";

  if (!verifyCredentials(username, password)) {
    return Response.json({ error: "Invalid credentials" }, { status: 401 });
  }

  await createSession();
  return Response.json({ success: true });
}
