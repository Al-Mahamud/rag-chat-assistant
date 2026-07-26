import "server-only";

import { timingSafeEqual } from "crypto";

function safeCompare(a: string, b: string): boolean {
  const bufA = Buffer.from(a);
  const bufB = Buffer.from(b);
  if (bufA.length !== bufB.length) {
    return false;
  }
  return timingSafeEqual(bufA, bufB);
}

export function verifyCredentials(username: string, password: string): boolean {
  const expectedUsername = process.env.BASIC_AUTH_USERNAME ?? "";
  const expectedPassword = process.env.BASIC_AUTH_PASSWORD ?? "";
  const validUser = safeCompare(username, expectedUsername);
  const validPass = safeCompare(password, expectedPassword);
  return validUser && validPass;
}
