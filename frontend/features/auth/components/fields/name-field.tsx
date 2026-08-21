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

export function NameField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "نام کامل" } = props;
	return (
		<Controller
			name={name}
			control={control}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid} dir="rtl">
					<FieldLabel htmlFor="form-name">{label}</FieldLabel>
					<Input
						{...field}
						autoFocus
						type="text"
						autoComplete="name"
						id="form-name"
						aria-invalid={fieldState.invalid}
						placeholder="نام کامل خود را وارد کنید"
					/>
					{fieldState.invalid && (
						<FieldError
							errors={[fieldState.error]}
							className="text-xs text-right"
						/>
					)}
				</Field>
			)}
		/>
	);
}
