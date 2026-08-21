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

export function PhoneNumberField<T extends FieldValues>(props: Props<T>) {
	const { control, name, label = "شماره همراه" } = props;
	return (
		<Controller
			name={name}
			control={control}
			render={({ field, fieldState }) => (
				<Field data-invalid={fieldState.invalid}>
					<FieldLabel htmlFor="form-phone-number">{label}</FieldLabel>
					<Input
						{...field}
						autoFocus
						dir="ltr"
						type="tel"
						autoComplete="mobile tel"
						id="form-phone-number"
						aria-invalid={fieldState.invalid}
						placeholder="09..."
						className="placeholder:text-left"
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
