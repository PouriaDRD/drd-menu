"use client";

import { useEffect, useState } from "react";

import { useTheme } from "next-themes";

/**
 * Hook to switch between light, dark, and system themes.
 */
export function useThemeSwitcher() {
	const [mounted, setMounted] = useState(false);
	const { theme, setTheme } = useTheme();

	// eslint-disable-next-line react-hooks/set-state-in-effect
	useEffect(() => setMounted(true), []);

	/**
	 * Get the next theme based on the current theme.
	 */
	const getNextTheme = () => {
		switch (theme) {
			case "light":
				return "dark";

			case "dark":
				return "system";

			case "system":
				return "light";

			default:
				return "light";
		}
	};

	/**
	 * Handles toggling the theme
	 */
	function handleToggle() {
		setTheme(getNextTheme());
	}

	return {
		theme,
		mounted,
		setTheme,
		handleToggle,
	};
}
