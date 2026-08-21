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

export function PasswordField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "رمز عبور" } = props;
	return (
		<Controller
			control={control}
			name={name}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid} className="w-full">
					<FieldLabel htmlFor="form-password">{label}</FieldLabel>

					<Input
						{...field}
						dir="ltr"
						type="password"
						id="form-password"
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
