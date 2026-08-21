"use client";

import { Activity } from "react";

import { cn } from "@/features/shared/utils";

import { AppIcon } from "./app-icon";

interface Props {
	text?: string;
	className?: string;
	hideLogoText?: boolean;
	hideLogoTextOnMobile?: boolean;
}

export default function AppLogo(props: Props) {
	const { className, hideLogoText, hideLogoTextOnMobile = true } = props;
	return (
		<div
			className={cn(
				"flex items-center justify-center text-center gap-4",
				className,
			)}>
			<Activity mode={hideLogoText ? "hidden" : "visible"}>
				<span
					suppressHydrationWarning
					className={cn(
						"font-bold text-xl md:text-2xl text-center font-mono!",
						`${hideLogoTextOnMobile && "hidden md:block"}`,
					)}>
					DRD Finance
				</span>
			</Activity>
			<div className="size-7 md:size-8">
				<AppIcon className="size-full" />
			</div>
		</div>
	);
}
