"use client";

import { useState } from "react";

import { toast } from "sonner";

import { useUser } from "@/features/accounts/context";

import { getRefreshToken, logoutAction } from "../actions";
import { useLogoutMutation } from "../mutations";

export function useLogout() {
	const [isLoading, setIsLoading] = useState(false);
	const { clearUser } = useUser();

	const logoutMutation = useLogoutMutation();

	const handleLogout = async () => {
		setIsLoading(true);
		try {
			const refreshToken = await getRefreshToken();

			if (refreshToken) {
				logoutMutation.mutate(
					{
						refresh: refreshToken,
					},
					{
						onSuccess: async (data) => {
							if (!data.success) {
								toast.error("خطا!", {
									description: "خطا در خارج شدن از سیستم",
								});
								return;
							}
							await logoutAction();
							clearUser();
							toast.success("با موفقیت خارج شدید", {
								description: "به امید دیدار!",
							});
							// eslint-disable-next-line @next/next/no-location-assign-relative-destination
							window.location.href = "/auth";
						},
						onError: async () => {
							toast.error("خطا!", {
								description: "خطا در خارج شدن از سیستم",
							});
							return;
						},
					},
				);
			}

			// clear user session
			// await logoutAction();
			// clearUser();
			// toast.success("با موفقیت خارج شدید");

			// redirect to login page
			// window.location.href = "/auth/login";
		} catch (error) {
			if (process.env.NODE_ENV === "development") {
				console.error("[LogoutAction]", error);
			}

			toast.error("خطا!", {
				description: "خطا در خارج شدن از سیستم",
			});
		} finally {
			setIsLoading(false);
		}
	};

	return {
		isLoading,
		handleLogout,
	};
}
