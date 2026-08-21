"use client";

import Link from "next/link";

import { ThemeSwitcher } from "@/features/preferences/components";

import AppLogo from "../icons/app-logo";
import { ScrollArea } from "../ui";

export function PanelHeader() {
	return (
		<ScrollArea>
			<header
				className={`bg-background/95 md:bg-sidebar/95 sticky top-0 z-50 
        	flex items-center justify-between gap-4
			border-b backdrop-blur-2xl px-4 py-2.5`}>
				<div className="flex items-center gap-4">
					<ThemeSwitcher />
				</div>
				<Link href={"/"}>
					<AppLogo />
				</Link>
			</header>{" "}
		</ScrollArea>
	);
}
