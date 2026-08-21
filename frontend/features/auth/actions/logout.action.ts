"use server";

import { clearSession } from "./session.action";

/**
 * Logout user action by deleting the session cookie
 */
export async function logoutAction(): Promise<void> {
	// Delete the session cookie
	await clearSession();
}
