import type { FieldPath, FieldValues, UseFormSetError } from "react-hook-form";

import type { ApiResponse } from "@/features/api/types";

/**
 * Apply backend validation errors
 * directly to React Hook Form.
 */
export function applyApiErrors<TFieldValues extends FieldValues>(
	response: ApiResponse,
	setError: UseFormSetError<TFieldValues>,
): boolean {
	if (response.success) {
		return false;
	}

	Object.entries(response.errors).forEach(([field, errors]) => {
		const error = errors[0];

		if (!error) {
			return;
		}

		setError(field as FieldPath<TFieldValues>, {
			type: error.code,
			message: error.message,
		});
	});

	return true;
}
