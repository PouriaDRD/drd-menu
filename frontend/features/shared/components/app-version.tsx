"use client";

import { cn } from "../utils";
import { getAppVersion } from "../utils/get-app-version";

interface AppVersionProps {
	className?: string;
}

const AppVersion = (props: AppVersionProps) => {
	const appVersion: string = getAppVersion();

	return (
		<div
			className={cn(
				`text-muted-foreground text-xs text-center w-full space-x-1 font-mono!`,
				props.className,
			)}>
			<span>نسخه</span>
			<span>{appVersion}</span>
		</div>
	);
};

export default AppVersion;
