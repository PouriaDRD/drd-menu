"use client";

import { useTheme } from "next-themes";

import { Toaster } from "@/components/ui";
import { ThemeType } from "@/features/preferences/types";

export const AppToaster = () => {
	const { theme = "system" } = useTheme();

	return <Toaster position="top-center" theme={theme as ThemeType} />;
};
