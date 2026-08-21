import { Fragment, PropsWithChildren } from "react";

import { Metadata } from "next";

export async function generateMetadata(): Promise<Metadata> {
	return {
		title: "ورود/ثبت‌نام",
		description: "ورود/ثبت‌نام به سایت",
	};
}

function LoginLayout({ children }: Readonly<PropsWithChildren>) {
	return <Fragment>{children}</Fragment>;
}

export default LoginLayout;
