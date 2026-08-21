import { ComponentType } from "react";

export type ThemeType = "light" | "dark" | "system";

export type Theme = {
	value: ThemeType;
	label: string;
	icon: ComponentType<{ className?: string }>;
};
