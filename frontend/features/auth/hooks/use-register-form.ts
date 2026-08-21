"use client";

import { useEffect, useEffectEvent } from "react";

import { useRouter, useSearchParams } from "next/navigation";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { useUser } from "@/features/user/context";

import { createSession } from "../actions";
import { useRegister } from "../mutations";
import { registerSchema } from "../schemas";
import { useRegisterStore } from "../stores";
import { RegisterData } from "../types";

interface Props {
	onSuccess?: () => void;
}

export function useRegisterForm({ onSuccess }: Props) {
	const router = useRouter();
	const searchParams = useSearchParams();
	const next = searchParams.get("next");

	const { refetchUser } = useUser();
	const registerMutation = useRegister();
	const registerStore = useRegisterStore();

	const form = useForm({
		resolver: zodResolver(registerSchema),
		defaultValues: {
			email: registerStore.email,
			name: "",
			password: "",
			confirm_password: "",
		},
	});

	const handleOnSuccess = async (data: RegisterData) => {
		await Promise.all([
			createSession({
				token: data.access,
				expireTimeUtc: data.access_expires_at,
				type: "acs",
			}),
			createSession({
				token: data.refresh,
				expireTimeUtc: data.refresh_expires_at,
				type: "rfs",
			}),
			refetchUser(),
		]);

		toast.success("حساب کاربری با موفقیت ایجاد شد!");

		form.reset();
		registerStore.reset();

		onSuccess?.();

		const redirectTo = next ?? "/panel/dashboard";

		router.push(redirectTo as "/");
	};

	const submit = form.handleSubmit(async (values) => {
		registerMutation.mutate(values, {
			onSuccess: async (res) => {
				if (!res.success) {
					toast.error(res.message || "خطا در ثبت نام");
					return;
				}

				await handleOnSuccess(res.data);
			},
			onError: () => {
				toast.error("خطا در ثبت نام");
			},
		});
	});

	/**
	 * Sync form values with zustand store
	 */
	useEffect(() => {
		// eslint-disable-next-line react-hooks/incompatible-library
		const subscription = form.watch((values) => {
			registerStore.set({
				email: values.email,
				name: values.name,
				password: values.password,
				confirm_password: values.confirm_password,
			});
		});

		return () => subscription.unsubscribe();
	}, [form, registerStore]);

	/**
	 * Restore form after zustand hydration
	 */
	const onHasHydrated = useEffectEvent(() => {
		form.reset({
			email: registerStore.email,
			name: registerStore.name,
			password: "",
			confirm_password: "",
		});
	});

	useEffect(() => {
		if (registerStore._hasHydrated) {
			onHasHydrated();
		}
	}, [registerStore._hasHydrated]);

	return {
		form,
		submit,
		isPending: registerMutation.isPending,
	};
}
