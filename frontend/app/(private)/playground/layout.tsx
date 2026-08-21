import { Fragment, PropsWithChildren } from "react";

import { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
	return {
		title: "زمین بازی",
		description: "تست یو آی و کامپوننت ها",
	};
}

export default function PlaygroundLayout({
	children,
}: Readonly<PropsWithChildren>) {
	return <Fragment>{children}</Fragment>;
}
