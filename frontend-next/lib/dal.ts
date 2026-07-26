import "server-only";

import { cookies } from "next/headers";
import { COOKIE_NAME, decrypt } from "./session";

export async function verifySession(): Promise<boolean> {
  const cookieStore = await cookies();
  const token = cookieStore.get(COOKIE_NAME)?.value;
  const session = await decrypt(token);
  return session?.authenticated === true;
}
