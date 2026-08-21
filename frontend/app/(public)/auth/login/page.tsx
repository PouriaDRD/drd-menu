"use client";

import Link from "next/link";

import { PageLayout } from "@/components/layouts";
import { Button } from "@/components/ui";
import { useUser } from "@/features/accounts/context";
import { LoginCard } from "@/features/auth/components/cards";
import { GridShape } from "@/features/shared/components";

function LoginPage() {
	const { user, isLoading } = useUser();

	if (isLoading) {
		return (
			<PageLayout className="flex items-center justify-center relative">
				<GridShape />
				<p
					suppressHydrationWarning
					className="text-sm text-muted-foreground">
					در حال بارگذاری...
				</p>
			</PageLayout>
		);
	}

	/**
	 * If user is already authenticated,
	 * redirect them away from register page.
	 */
	if (user) {
		return (
			<PageLayout className="flex items-center justify-center relative">
				<GridShape />
				<AlreadyLoggedIn />
			</PageLayout>
		);
	}

	return (
		<PageLayout className="flex items-center justify-center relative">
			<GridShape />
			<LoginCard />
		</PageLayout>
	);
}

export default LoginPage;

/**
 * UI shown when user is already authenticated.
 */
function AlreadyLoggedIn() {
	return (
		<div className="flex flex-col items-center gap-4 text-center bg-card shadow p-6 rounded-2xl">
			<p
				suppressHydrationWarning
				className="text-sm text-muted-foreground">
				شما قبلاً وارد شده‌اید و نیازی به ورود ندارید.
			</p>

			<Link href="/panel/dashboard">
				<Button variant={"outline"} size={"sm"}>
					بازگشت به پنل
				</Button>
			</Link>
		</div>
	);
}
