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

export function EmailField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "ایمیل" } = props;
	return (
		<Controller
			name={name}
			control={control}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid}>
					<FieldLabel htmlFor="form-email">{label}</FieldLabel>
					<Input
						{...field}
						autoFocus
						dir="ltr"
						type="email"
						autoComplete="email"
						id="form-email"
						aria-invalid={fieldState.invalid}
						placeholder="example@example.com"
						className="placeholder:text-right"
					/>
					{fieldState.invalid && (
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
