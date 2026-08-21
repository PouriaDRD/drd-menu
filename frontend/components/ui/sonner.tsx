"use client";

import * as React from "react";

import { useTheme } from "next-themes";

import {
	CircleCheckIcon,
	InfoIcon,
	Loader2Icon,
	OctagonXIcon,
	TriangleAlertIcon,
} from "lucide-react";
import { Toaster as Sonner, type ToasterProps } from "sonner";

const Toaster = ({ ...props }: ToasterProps) => {
	const { theme = "system" } = useTheme();

	return (
		<Sonner
			theme={theme as ToasterProps["theme"]}
			position="bottom-right"
			gap={6}
			duration={2500}
			icons={{
				success: (
					<CircleCheckIcon className="size-4" strokeWidth={1.7} />
				),

				info: <InfoIcon className="size-4" strokeWidth={1.7} />,

				warning: (
					<TriangleAlertIcon className="size-4" strokeWidth={1.7} />
				),

				error: <OctagonXIcon className="size-4" strokeWidth={1.7} />,

				loading: (
					<Loader2Icon
						className="size-4 animate-spin"
						strokeWidth={1.7}
					/>
				),
			}}
			{...props}
		/>
	);
};

export { Toaster };
