import { verifySession } from "@/lib/dal";
import { getBackendAuthHeader, getBackendUrl } from "@/lib/backend";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const authenticated = await verifySession();
  if (!authenticated) {
    return Response.json({ detail: "Unauthorized" }, { status: 401 });
  }

  const incomingForm = await request.formData().catch(() => null);
  const file = incomingForm?.get("file");
  if (!file || !(file instanceof File)) {
    return Response.json({ detail: "A PDF file is required." }, { status: 400 });
  }

  // Build a fresh FormData rather than forwarding the parsed one directly, and
  // let fetch generate its own multipart boundary — do not set Content-Type
  // manually, or the backend will fail to parse the body.
  const outgoingForm = new FormData();
  outgoingForm.append("file", file, file.name);

  const backendResponse = await fetch(`${getBackendUrl()}/upload`, {
    method: "POST",
    headers: {
      Authorization: getBackendAuthHeader(),
    },
    body: outgoingForm,
  });

  const data = await backendResponse.json().catch(() => ({}));
  return Response.json(data, { status: backendResponse.status });
}
