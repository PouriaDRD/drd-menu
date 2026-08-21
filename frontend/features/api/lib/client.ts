import { ApiResponse } from "@/features/api/types";
import { getSession, refreshAccessToken } from "@/features/auth/actions";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_API_URL?.trim() ?? "";

type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface RequestProps {
	url: string;
	method: HttpMethod;
	body?: unknown;
	params?: Record<string, string | number | boolean | undefined>;
	init?: RequestInit;
	timeout?: number;
	isMultipart?: boolean;
	retry?: boolean;
}

/**
 * API CLIENT
 */
class ApiClient {
	// =========================================================
	// MAIN REQUEST
	// =========================================================

	private async request<T>(props: RequestProps): Promise<ApiResponse<T>> {
		const {
			url,
			method,
			body,
			params,
			init,
			timeout = 60000, // 60 seconds
			isMultipart = false,
			retry = true,
		} = props;

		const controller = new AbortController();
		const timer = setTimeout(() => controller.abort(), timeout);

		try {
			const finalUrl = buildApiUrl(url, params);

			const headers: Record<string, string> = {
				...(init?.headers as Record<string, string>),
			};

			// Add auth token automatically
			const token = await this.getToken();
			if (token) {
				headers["Authorization"] = `Bearer ${token}`;
			}

			// Content-Type handling
			if (!isMultipart) {
				headers["Content-Type"] = "application/json";
			}

			const response = await fetch(finalUrl, {
				method,
				headers,
				signal: controller.signal,
				body: this.buildBody(body, isMultipart),
				...init,
			});

			clearTimeout(timer);

			//Handle Too Many Requests (429)
			if (response.status === 429) {
				return {
					success: false,
					message: "درخواست بیش از حد مجاز است",

					errors: "لطفا چند لحظه بعد دوباره تلاش کنید",
				};
			}

			// =========================
			// Handle Unauthorized (401)
			// =========================
			if (response.status === 401 && retry) {
				const refreshed = await this.refreshToken();

				if (refreshed) {
					return this.request<T>({
						url,
						method,
						body,
						params,
						init,
						timeout,
						isMultipart,
						retry: false,
					});
				}
			}

			return await response.json();
		} catch (err: unknown) {
			clearTimeout(timer);

			if (process.env.NODE_ENV === "development") {
				console.error("Error[apiClient.request]:", err);
			}

			const errorName =
				err instanceof Error
					? err.name
					: typeof err === "object" && err !== null && "name" in err
						? String((err as { name?: unknown }).name)
						: undefined;

			if (errorName === "AbortError") {
				return {
					success: false,
					message: "درخواست بیش از حد طول کشید",
					errors: "درخواست بیش از حد طول کشید",
				};
			}

			return {
				success: false,
				message: "خطای ناخواسته رخ داده است",
				errors: "خطای ناخواسته رخ داده است",
			};
		}
	}

	// =========================================================
	// HTTP METHODS
	// =========================================================

	get<T>(url: string, params?: RequestProps["params"], init?: RequestInit) {
		return this.request<T>({ url, method: "GET", params, init });
	}

	post<T>(
		url: string,
		body?: unknown,
		init?: RequestInit,
		isMultipart = false,
	) {
		return this.request<T>({
			url,
			method: "POST",
			body,
			init,
			isMultipart,
		});
	}

	put<T>(url: string, body?: unknown, init?: RequestInit) {
		return this.request<T>({ url, method: "PUT", body, init });
	}

	patch<T>(url: string, body?: unknown, init?: RequestInit) {
		return this.request<T>({ url, method: "PATCH", body, init });
	}

	delete<T>(url: string, init?: RequestInit) {
		return this.request<T>({ url, method: "DELETE", init });
	}

	// =========================================================
	// TOKEN
	// =========================================================

	/**
	 * Simple helper to get cookies (Next.js compatible client-side)
	 */
	private async getToken(): Promise<string | null> {
		const token = await getSession();
		return token || null;
	}

	/**
	 * Refresh access token automatically
	 */
	private async refreshToken(): Promise<boolean> {
		try {
			const newAccess = await refreshAccessToken();

			if (newAccess) {
				return true;
			}

			return false;
		} catch {
			return false;
		}
	}

	// =========================================================
	// BODY BUILDER
	// =========================================================

	private buildBody(body: unknown, isMultipart?: boolean) {
		if (!body) return undefined;

		// FormData (file upload)
		if (isMultipart && body instanceof FormData) {
			return body;
		}

		return JSON.stringify(body);
	}
}

export const apiClient = new ApiClient();

/**
 * Build final URL safely
 */
export function buildApiUrl(
	path: string,
	params?: Record<string, string | number | boolean | undefined>,
): string {
	const base = BASE_URL.replace(/\/+$/, "");

	const cleanPath = path.replace(/^\/+/, "").replace(/\/+$/, "");

	const isAbsolute = /^https?:\/\//i.test(path);

	const url = isAbsolute
		? new URL(path)
		: new URL(`${cleanPath}/`, `${base}/`);

	if (params) {
		Object.entries(params).forEach(([key, value]) => {
			if (value !== undefined && value !== null) {
				url.searchParams.append(key, String(value));
			}
		});
	}

	return url.toString();
}
