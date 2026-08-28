"use client";

import { Button, FieldGroup, Spinner } from "@/components/ui";
import { NameField } from "@/features/auth/components/fields";

import { useProfileForm } from "../../hooks/use-profile-form";
import { ProfileFormValues } from "../../types";

interface Props {
	initialValues?: ProfileFormValues;
	onSuccess?: (data: ProfileFormValues) => void;
}

export function UpdateProfileForm({ initialValues, onSuccess }: Props) {
	const { form, submit, isPending } = useProfileForm({
		initialValues,
		onSuccess(data) {
			onSuccess?.(data);
		},
	});

	return (
		<form id="profile-name-form" onSubmit={submit}>
			<FieldGroup>
				<NameField control={form.control} name="first_name" />

				<NameField control={form.control} name="last_name" />
			</FieldGroup>

			<Button
				type="submit"
				form="profile-name-form"
				className="w-full mt-6"
				disabled={isPending}>
				{isPending ? <Spinner /> : "ذخیره تغییرات"}
			</Button>
		</form>
	);
}
