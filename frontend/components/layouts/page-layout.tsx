"use client";

import { cn } from "@/features/shared/utils";

interface Props {
	className?: string;
	children?: React.ReactNode;
}

export function PageLayout({ children, className }: Props) {
	return (
		<main
			className={cn(
				"flex-1 h-full w-full px-4 py-4 sm:px-8 sm:py-8",
				className,
			)}>
			{children}
		</main>
	);
}
