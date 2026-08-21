/**
 * Base success response.
 */
export interface ApiSuccessResponse<T = unknown> {
	success: true;
	message: string;
	data: T;
}

export type ApiError = string | Record<string, string | string[] | unknown>;

/**
 * Base error response.
 */
export interface ApiErrorResponse {
	success: false;
	message: string;
	error: ApiError;
}

/**
 * Union of all API responses.
 */
export type ApiResponse<T = unknown> = ApiSuccessResponse<T> | ApiErrorResponse;
