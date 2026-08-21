export interface ApiFieldError {
	message: string;
	code: ApiErrorCode;
}

export type ApiErrors = Record<string, ApiFieldError[]>;

export interface ApiSuccessResponse<T = unknown> {
	success: true;

	code: "SUCCESS";

	message: string;

	data: T;

	errors: null;
}

export interface ApiErrorResponse {
	success: false;

	code: ApiErrorCode;

	message: string;

	data: [];

	errors: ApiErrors;
}

export type ApiResponse<T = unknown> = ApiSuccessResponse<T> | ApiErrorResponse;

export const API_ERROR_CODES = {
	SUCCESS: "SUCCESS",

	// Authentication
	NOT_AUTHENTICATED: "NOT_AUTHENTICATED",
	PERMISSION_DENIED: "PERMISSION_DENIED",
	AUTHENTICATION_ERROR: "AUTHENTICATION_ERROR",

	ACCOUNT_DISABLED: "ACCOUNT_DISABLED",
	ACCOUNT_NOT_FOUND: "ACCOUNT_NOT_FOUND",

	// Server
	NOT_FOUND: "NOT_FOUND",
	THROTTLED: "THROTTLED",
	SERVER_ERROR: "SERVER_ERROR",
	NETWORK_ERROR: "NETWORK_ERROR",
	REQUEST_TIMEOUT: "REQUEST_TIMEOUT",

	// Validation
	INVALID_CREDENTIALS: "INVALID_CREDENTIALS",

	VALIDATION_ERROR: "VALIDATION_ERROR",

	LAST_NAME_TOO_SHORT: "LAST_NAME_TOO_SHORT",
	FIRST_NAME_TOO_SHORT: "FIRST_NAME_TOO_SHORT",
	INVALID_PHONE_NUMBER: "INVALID_PHONE_NUMBER",

	EMAIL_ALREADY_EXISTS: "EMAIL_ALREADY_EXISTS",
	PHONE_ALREADY_EXISTS: "PHONE_ALREADY_EXISTS",
	USERNAME_ALREADY_EXISTS: "USERNAME_ALREADY_EXISTS",
} as const;

export type ApiErrorCode =
	(typeof API_ERROR_CODES)[keyof typeof API_ERROR_CODES];
