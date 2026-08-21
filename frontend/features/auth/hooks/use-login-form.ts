"use client";

import { useEffect, useEffectEvent } from "react";

import { useRouter, useSearchParams } from "next/navigation";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { useUser } from "@/features/accounts/context";
import { getApiErrorMessage } from "@/features/api/utils";

import { createSession } from "../actions";
import { useLogin } from "../mutations";
import { loginSchema } from "../schemas";
import { useLoginStore } from "../stores";
import { LoginData } from "../types";

interface Props {
	onSuccess?: () => void;
}

export function useLoginForm({ onSuccess }: Props) {
	// Router
	const router = useRouter();
	const searchParams = useSearchParams();
	const next = searchParams.get("next");

	const { refetchUser } = useUser();
	const loginMutation = useLogin();
	const loginStore = useLoginStore();

	const form = useForm({
		resolver: zodResolver(loginSchema),
		defaultValues: {
			phone_number: loginStore.phone_number,
			password: "",
		},
	});

	const handleOnSuccess = async (data: LoginData) => {
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
		toast.success("خوش آمدید!", {
			description: "با موفقیت به حساب خود وارد شدید.",
		});

		// Reset form and store
		form.reset();
		loginStore.reset();

		onSuccess?.();

		const redirectTo = next ?? "/panel/user";
		router.push(redirectTo as "/");
	};

	const submit = form.handleSubmit(async (values) => {
		loginMutation.mutate(values, {
			onSuccess: async (response) => {
				if (response.success) {
					await handleOnSuccess(response.data);
					return;
				}

				toast.error("خطا!", {
					description: getApiErrorMessage(response.code),
				});
			},
			onError: () => {
				toast.error("خطا!", {
					description: "اطلاعات وارد شده صحیح نیست.",
				});
			},
		});
	});

	// Sync form -> store
	useEffect(() => {
		// eslint-disable-next-line react-hooks/incompatible-library
		const subscription = form.watch(async (values) => {
			loginStore.set({
				phone_number: values.phone_number,
				password: values.password,
			});
		});
		return () => subscription.unsubscribe();
	}, [form, loginStore]);

	const onHasHydrated = useEffectEvent(() => {
		form.reset({
			phone_number: loginStore.phone_number,
			password: "",
		});
	});

	// Reset form from store on mount
	useEffect(() => {
		if (loginStore._hasHydrated) {
			onHasHydrated();
		}
	}, [loginStore._hasHydrated]);

	return {
		form,
		submit,
		isPending: loginMutation.isPending,
	};
}
