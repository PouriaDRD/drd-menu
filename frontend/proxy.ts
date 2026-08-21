import { type NextRequest, NextResponse } from "next/server";

import { getSession } from "./features/auth/actions";

export async function proxy(request: NextRequest) {
	const next = `${request.nextUrl.pathname}${request.nextUrl.search}`;

	const redirectUrl = new URL("/auth", request.url);

	redirectUrl.searchParams.set("next", next);

	try {
		const session = await getSession();

		if (!session) {
			return NextResponse.redirect(redirectUrl, { status: 303 });
		}

		return NextResponse.next();
	} catch (error) {
		if (process.env.NODE_ENV === "development") {
			console.error("Error during proxy:", error);
		}

		return NextResponse.redirect(redirectUrl, { status: 303 });
	}
}

export const config = {
	matcher: ["/user/:path*"],
};
