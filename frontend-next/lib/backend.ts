import "server-only";

export function getBackendUrl(): string {
  const url = process.env.BACKEND_URL;
  if (!url) {
    throw new Error("BACKEND_URL is not set.");
  }
  return url;
}

export function getBackendAuthHeader(): string {
  const username = process.env.BASIC_AUTH_USERNAME ?? "";
  const password = process.env.BASIC_AUTH_PASSWORD ?? "";
  return "Basic " + Buffer.from(`${username}:${password}`).toString("base64");
}
