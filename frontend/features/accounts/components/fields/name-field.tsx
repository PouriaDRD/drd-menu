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

export function FirstNameField<T extends FieldValues>({
	control,
	name,
	label = "نام",
}: Props<T>) {
	return (
		<Controller
			name={name}
			control={control}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid}>
					<FieldLabel>{label}</FieldLabel>

					<Input
						{...field}
						placeholder="نام"
						aria-invalid={fieldState.invalid}
					/>

					{fieldState.error && (
						<FieldError errors={[fieldState.error]} />
					)}
				</Field>
			)}
		/>
	);
}
