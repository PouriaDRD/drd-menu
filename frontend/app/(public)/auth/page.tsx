"use client";

import { PageLayout } from "@/components/layouts";
import { useUser } from "@/features/accounts/context";
import { LoginCard } from "@/features/auth/components/cards";
import {
	AlreadyLoggedIn,
	GridShape,
	LoadingCard,
} from "@/features/shared/components";

export default function AuthPage() {
	const { user, isLoading } = useUser();

	if (isLoading) {
		return <LoadingCard />;
	}

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
			<LoginCard className="ring-0 border-0 bg-transparent shadow-none" />
		</PageLayout>
	);
}
