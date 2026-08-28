"use client";

import { PageLayout } from "@/components/layouts";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { SimpleUserCard } from "@/features/accounts/components/cards";
import { UpdateProfileResponsive } from "@/features/accounts/components/dialogs";
import { useUser } from "@/features/accounts/context";
import { LogoutDialog } from "@/features/auth/components/dialogs";
import { LoginHistoryTable } from "@/features/auth/components/tables";
import {
	GridShape,
	LoadingCard,
	UserPageError,
} from "@/features/shared/components";

export default function UserPage() {
	const { user, isLoading } = useUser();

	// Loading State
	if (isLoading) {
		return <LoadingCard />;
	}

	// Error State
	if (!user) {
		return (
			<UserPageError
				error={new Error("اطلاعات کاربر در دسترس نیست")}
				onRetry={() => window.location.reload()}
			/>
		);
	}

	return (
		<PageLayout className="container relative mx-auto max-w-6xl space-y-6 px-4 py-8">
			<GridShape />

			{/* Page Header */}
			<div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
				<div>
					<h1 className="text-2xl font-bold tracking-tight text-foreground">
						پروفایل کاربری
					</h1>
					<p className="mt-1 text-xs text-muted-foreground sm:text-sm">
						مدیریت اطلاعات حساب کاربری و بررسی نشست‌های فعال
					</p>
				</div>

				{/* Actions Toolbar */}
				<div className="flex items-center gap-2.5">
					<UpdateProfileResponsive
						initialValues={{
							first_name: user.first_name,
							last_name: user.last_name,
						}}
					/>
					<LogoutDialog variant="outline" />
				</div>
			</div>

			{/* Main Dashboard Layout */}
			<div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-3">
				{/* User Info Card Sidebar */}
				<div className="lg:col-span-1">
					<SimpleUserCard user={user} />
				</div>

				{/* Login History Section Card */}
				<div className="lg:col-span-2">
					<Card className="overflow-hidden border-border/60 shadow-sm">
						<CardHeader className="border-b bg-muted/20 px-6 py-4">
							<CardTitle className="text-base font-semibold">
								تاریخچه ورود به سیستم
							</CardTitle>
							<CardDescription className="text-xs">
								فهرست آخرین نشست‌ها و زمان‌های ورود فعال به حساب
								کاربری شما
							</CardDescription>
						</CardHeader>
						<CardContent className="p-0">
							<LoginHistoryTable />
						</CardContent>
					</Card>
				</div>
			</div>
		</PageLayout>
	);
}
