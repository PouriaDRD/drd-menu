import { Fragment, PropsWithChildren } from "react";

import { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
	return {
		title: "Playground",
		description: "Playground for testing components",
	};
}

export default function PlaygroundLayout({
	children,
}: Readonly<PropsWithChildren>) {
	return <Fragment>{children}</Fragment>;
}
