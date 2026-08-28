"use client";

import { useEffect } from "react";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { toast } from "sonner";

import { queryClient, queryKeys } from "@/features/api/lib";
import { getApiErrorMessage } from "@/features/api/utils";

import { useUpdateProfile } from "../mutations";
import { updateProfileSchema } from "../schemas";
import { ProfileFormValues } from "../types";

interface Props {
	initialValues?: ProfileFormValues;
	onSuccess?: (data: ProfileFormValues) => void;
}

export function useProfileForm({ initialValues, onSuccess }: Props) {
	const mutation = useUpdateProfile();

	const form = useForm<ProfileFormValues>({
		resolver: zodResolver(updateProfileSchema),
		defaultValues: {
			first_name: initialValues?.first_name ?? "",
			last_name: initialValues?.last_name ?? "",
		},
	});

	// Keep form values in sync when initialValues change
	useEffect(() => {
		if (initialValues) {
			form.reset({
				first_name: initialValues.first_name ?? "",
				last_name: initialValues.last_name ?? "",
			});
		}
	}, [initialValues, form]);

	const handleOnSuccess = async (data: ProfileFormValues) => {
		await Promise.all([
			queryClient.invalidateQueries({
				queryKey: queryKeys.accounts.myProfile,
			}),
		]);

		toast.success("عملیات موفق بود", {
			description: "اطلاعات شما با موفقیت ذخیره شد.",
		});

		onSuccess?.(data);
	};

	const submit = form.handleSubmit((values) => {
		mutation.mutate(values, {
			onSuccess: async (response) => {
				if (response.success) {
					await handleOnSuccess(response.data);
					return;
				}

				const firstNameError = response.errors.first_name?.[0];

				if (firstNameError) {
					form.setError("first_name", {
						message: getApiErrorMessage(firstNameError.code),
					});
				}

				const lastNameError = response.errors.last_name?.[0];

				if (lastNameError) {
					form.setError("last_name", {
						message: getApiErrorMessage(lastNameError.code),
					});
				}

				toast.error("خطا!", {
					description: getApiErrorMessage(response.code),
				});
			},
		});
	});

	return {
		form,
		submit,
		isPending: mutation.isPending,
	};
}
