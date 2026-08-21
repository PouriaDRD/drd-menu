"use client";

import { Button, FieldGroup, Spinner } from "@/components/ui";

import { useRegisterForm } from "../../hooks";
import {
	ConfirmPasswordField,
	EmailField,
	NameField,
	PasswordField,
} from "../fields";

interface Props {
	onSuccess?: () => void;
}

function RegisterForm({ onSuccess }: Props) {
	const { form, submit, isPending } = useRegisterForm({
		onSuccess() {
			onSuccess?.();
		},
	});

	return (
		<form id="register-form" onSubmit={submit}>
			<FieldGroup>
				{/* Email Name */}
				<EmailField control={form.control} name="email" label="ایمیل" />

				{/* Referral Code */}
				<NameField
					control={form.control}
					name="name"
					label="نام کامل"
				/>

				{/* Password */}
				<PasswordField
					control={form.control}
					name="password"
					label="رمز عبور"
				/>

				{/* Confirm Password */}
				<ConfirmPasswordField
					control={form.control}
					name="confirm_password"
					label="تکرار رمز عبور"
				/>
			</FieldGroup>

			<Button
				type="submit"
				form="register-form"
				className="w-full mt-6"
				disabled={isPending}>
				{isPending ? <Spinner /> : "ثبت نام"}
			</Button>
		</form>
	);
}

export default RegisterForm;
