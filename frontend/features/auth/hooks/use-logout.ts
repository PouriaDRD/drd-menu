"use client";

import { useState } from "react";

import { toast } from "sonner";

import { useUser } from "@/features/user/context";

import { logoutAction } from "../actions";

export function useLogout() {
	const [isLoading, setIsLoading] = useState(false);
	const { clearUser } = useUser();

	const handleLogout = async () => {
		setIsLoading(true);
		try {
			// clear user session
			await logoutAction();
			clearUser();
			// redirect to login page
			toast.success("با موفقیت خارج شدید");

			// eslint-disable-next-line @next/next/no-location-assign-relative-destination
			window.location.href = "/auth/login";
		} catch (error) {
			if (process.env.NODE_ENV === "development") {
				console.error("[LogoutAction]", error);
			}

			toast.error("خطایی رخ داده است. لطفا مجددا تلاش کنید.");
		} finally {
			setIsLoading(false);
		}
	};

	return {
		isLoading,
		handleLogout,
	};
}
