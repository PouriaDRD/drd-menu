"use client";

import {
	type Control,
	Controller,
	type FieldValues,
	type Path,
} from "react-hook-form";

import { Field, FieldError, FieldLabel, Input } from "@/components/ui";

type Props<T extends FieldValues> = {
	control: Control<T>;
	name: Path<T>;
	label?: string;
};

export function ConfirmPasswordField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "تکرار رمز عبور" } = props;
	return (
		<Controller
			control={control}
			name={name}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid} className="w-full">
					<FieldLabel htmlFor="form-confirm-password">
						{label}
					</FieldLabel>

					<Input
						{...field}
						dir="ltr"
						type="password"
						id="form-confirm-password"
						autoComplete="new-password"
						aria-invalid={fieldState.invalid}
						placeholder="حداقل 8 کاراکتر"
						className="placeholder:text-right"
					/>

					{fieldState.error && (
						<FieldError
							errors={[fieldState.error]}
							className="text-xs"
						/>
					)}
				</Field>
			)}
		/>
	);
}
