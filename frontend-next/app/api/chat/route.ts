import { verifySession } from "@/lib/dal";
import { getBackendAuthHeader, getBackendUrl } from "@/lib/backend";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const authenticated = await verifySession();
  if (!authenticated) {
    return Response.json({ detail: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json().catch(() => null);
  if (!body || typeof body.query !== "string") {
    return Response.json({ detail: "Query must not be empty." }, { status: 400 });
  }

  const backendResponse = await fetch(`${getBackendUrl()}/chat`, {
    method: "POST",
    headers: {
      Authorization: getBackendAuthHeader(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query: body.query }),
  });

  const data = await backendResponse.json().catch(() => ({}));
  return Response.json(data, { status: backendResponse.status });
}
