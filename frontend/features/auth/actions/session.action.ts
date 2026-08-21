"use server";

import { cookies } from "next/headers";

import { buildApiUrl, endpoints } from "@/features/api/lib";

// ============================
// Helpers
// ============================

function calculateMaxAgeFromUtc(expireTimeUtc: Date): number {
	const now = Math.floor(Date.now() / 1000);
	const exp = Math.floor(new Date(expireTimeUtc).getTime() / 1000);

	// subtract 5s safety buffer
	return Math.max(exp - now - 5, 0);
}

// ============================
// Session Management
// ============================
interface CreateSessionProps {
	token: string;
	type: "acs" | "rfs";
	expireTimeUtc: Date;
}
/**
 * Create session from API response
 */
export async function createSession(props: CreateSessionProps) {
	const { token, type, expireTimeUtc } = props;
	try {
		const cookieStore = await cookies();

		const maxAge = calculateMaxAgeFromUtc(expireTimeUtc);

		cookieStore.set({
			name: type,
			value: token,
			httpOnly: true,
			secure: true,
			sameSite: "lax",
			path: "/",
			maxAge,
		});
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("[createSession]", error);
		}
	}
}

/**
 * Get valid access token (auto refresh if needed)
 */
export async function getSession(): Promise<string | null> {
	try {
		// test delay to simulate network latency
		// await new Promise((resolve) => setTimeout(resolve, 2000));

		const cookieStore = await cookies();

		let session = cookieStore.get("acs")?.value ?? null;

		if (!session) {
			session = await refreshAccessToken();
		}
		return session;
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("[getSession]", error);
		}
		return null;
	}
}

/**
 * Clear session cookies
 */
export async function clearSession(): Promise<void> {
	const cookieStore = await cookies();

	cookieStore.delete("acs");
	cookieStore.delete("rfs");
	cookieStore.delete("csrftoken");
}

/**
 * Call backend refresh endpoint
 */
export async function refreshAccessToken(): Promise<string | null> {
	try {
		const cookieStore = await cookies();

		const refreshToken = cookieStore.get("rfs")?.value;

		if (!refreshToken) {
			await clearSession();
			return null;
		}

		const res = await fetch(buildApiUrl(endpoints.auth.refresh), {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				refresh: refreshToken,
			}),
		});

		if (!res.ok) {
			await clearSession();
			return null;
		}

		const data = await res.json();
		const access = data.data.access;
		const expireTimeUtc = data.data.access_expires_at;

		await createSession({
			token: access,
			type: "acs",
			expireTimeUtc: expireTimeUtc,
		});

		return access;
	} catch (err) {
		if (process.env.NODE_ENV === "development") {
			console.error("[refreshAccessToken]", err);
		}
		await clearSession();
		return null;
	}
}
