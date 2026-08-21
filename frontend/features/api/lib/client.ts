import type { ApiResponse } from "@/features/api/types";
import { getSession, refreshAccessToken } from "@/features/auth/actions";

const BASE_URL = process.env.NEXT_PUBLIC_BASE_API_URL?.trim() ?? "";

type HttpMethod = "GET" | "POST" | "PATCH" | "DELETE";

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
			timeout = 60000,
			isMultipart = false,
			retry = true,
		} = props;

		const controller = new AbortController();

		const timer = setTimeout(() => controller.abort(), timeout);

		try {
			const finalUrl = buildApiUrl(url, params);

			const headers = new Headers(init?.headers);

			// =====================================================
			// AUTHORIZATION
			// =====================================================

			const token = await this.getToken();

			if (token) {
				headers.set("Authorization", `Bearer ${token}`);
			}

			// =====================================================
			// CONTENT TYPE
			// =====================================================

			if (!isMultipart) {
				headers.set("Content-Type", "application/json");
			}

			const response = await fetch(finalUrl, {
				...init,
				method,
				headers,
				signal: controller.signal,
				body: this.buildBody(body, isMultipart),
			});

			clearTimeout(timer);

			// =====================================================
			// UNAUTHORIZED
			// =====================================================

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

			// =====================================================
			// EMPTY RESPONSE
			// =====================================================

			if (response.status === 204) {
				return {
					success: true,
					code: "SUCCESS",
					message: "Operation completed successfully.",
					data: null as T,
					errors: null,
				};
			}

			// =====================================================
			// JSON RESPONSE
			// =====================================================

			const data: unknown = await response.json();

			return normalizeApiResponse<T>(data, response.status);
		} catch (error: unknown) {
			clearTimeout(timer);

			if (process.env.NODE_ENV === "development") {
				console.error("Error[apiClient.request]:", error);
			}

			const errorName =
				error instanceof Error
					? error.name
					: typeof error === "object" &&
						  error !== null &&
						  "name" in error
						? String(
								(
									error as {
										name?: unknown;
									}
								).name,
							)
						: undefined;

			// =====================================================
			// TIMEOUT
			// =====================================================

			if (errorName === "AbortError") {
				return {
					success: false,
					code: "REQUEST_TIMEOUT",
					message: "درخواست بیش از حد طول کشید.",
					data: [],
					errors: {
						request: [
							{
								message: "درخواست بیش از حد طول کشید.",
								code: "REQUEST_TIMEOUT",
							},
						],
					},
				};
			}

			// =====================================================
			// NETWORK ERROR
			// =====================================================

			return {
				success: false,
				code: "NETWORK_ERROR",
				message: "ارتباط با سرور برقرار نشد.",
				data: [],
				errors: {
					request: [
						{
							message: "ارتباط با سرور برقرار نشد.",
							code: "NETWORK_ERROR",
						},
					],
				},
			};
		}
	}

	// =========================================================
	// HTTP METHODS
	// =========================================================

	get<T>(url: string, params?: RequestProps["params"], init?: RequestInit) {
		return this.request<T>({
			url,
			method: "GET",
			params,
			init,
		});
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

	patch<T>(url: string, body?: unknown, init?: RequestInit) {
		return this.request<T>({
			url,
			method: "PATCH",
			body,
			init,
		});
	}

	delete<T>(url: string, init?: RequestInit) {
		return this.request<T>({
			url,
			method: "DELETE",
			init,
		});
	}

	// =========================================================
	// TOKEN
	// =========================================================

	private async getToken(): Promise<string | null> {
		const token = await getSession();

		return token || null;
	}

	private async refreshToken(): Promise<boolean> {
		try {
			const newAccess = await refreshAccessToken();

			return Boolean(newAccess);
		} catch {
			return false;
		}
	}

	// =========================================================
	// BODY
	// =========================================================

	private buildBody(
		body: unknown,
		isMultipart = false,
	): BodyInit | undefined {
		if (body === undefined || body === null) {
			return undefined;
		}

		if (isMultipart && body instanceof FormData) {
			return body;
		}

		return JSON.stringify(body);
	}
}

// =============================================================
// NORMALIZE API RESPONSE
// =============================================================

function normalizeApiResponse<T>(
	data: unknown,
	statusCode: number,
): ApiResponse<T> {
	if (isApiResponse<T>(data)) {
		return data;
	}

	if (statusCode >= 200 && statusCode <= 299) {
		return {
			success: true,
			code: "SUCCESS",
			message: "Operation completed successfully.",
			data: data as T,
			errors: null,
		};
	}

	return {
		success: false,
		code: "UNKNOWN_ERROR",
		message: "An unexpected error occurred.",
		data: [],
		errors: {
			request: [
				{
					message: "An unexpected error occurred.",
					code: "UNKNOWN_ERROR",
				},
			],
		},
	};
}

// =============================================================
// TYPE GUARD
// =============================================================

function isApiResponse<T>(value: unknown): value is ApiResponse<T> {
	if (typeof value !== "object" || value === null) {
		return false;
	}

	const object = value as Record<string, unknown>;

	return (
		typeof object.success === "boolean" &&
		typeof object.code === "string" &&
		typeof object.message === "string" &&
		"data" in object &&
		"errors" in object
	);
}

// =============================================================
// EXPORT
// =============================================================

export const apiClient = new ApiClient();

// =============================================================
// BUILD URL
// =============================================================

export function buildApiUrl(
	path: string,
	params?: Record<string, string | number | boolean | undefined>,
): string {
	const base = BASE_URL.replace(/\/+$/, "");

	const isAbsolute = /^https?:\/\//i.test(path);

	const url = isAbsolute
		? new URL(path)
		: new URL(
				`${path.replace(/^\/+/, "").replace(/\/+$/, "")}/`,
				`${base}/`,
			);

	if (params) {
		Object.entries(params).forEach(([key, value]) => {
			if (value !== undefined && value !== null) {
				url.searchParams.append(key, String(value));
			}
		});
	}

	return url.toString();
}
