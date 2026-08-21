"use client";

import { AlertCircle, RefreshCw } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import {
	SimpleUserCard,
	UpdateProfileCard,
} from "@/features/accounts/components/cards";
import { useUser } from "@/features/accounts/context";
import { LogoutDialog } from "@/features/auth/components/dialogs";
import { GridShape } from "@/features/shared/components";

export default function UserPage() {
	const { user, isLoading } = useUser();

	// Loading State
	if (isLoading) {
		return (
			<main className="relative flex min-h-dvh flex-col items-center justify-center text-center gap-4">
				<GridShape />
				<UserPageSkeleton />
			</main>
		);
	}

	// No User (shouldn't happen if error is handled)
	if (!user) {
		return (
			<main className="relative flex min-h-dvh flex-col items-center justify-center text-center gap-4">
				<GridShape />
				<UserPageError
					error={new Error("User data not available")}
					onRetry={window.location.reload}
				/>
			</main>
		);
	}

	return (
		<main
			className={`relative flex min-h-dvh flex-col md:flex-row items-center
        	justify-center text-center gap-4`}>
			<GridShape />

			<SimpleUserCard user={user} />

			<div className="w-full max-w-xs space-y-4">
				<UpdateProfileCard />

				<div className="w-full">
					<LogoutDialog className="w-full text-center" />
				</div>
			</div>
		</main>
	);
}

// ============================================
// LOADING STATE COMPONENT
// ============================================
function UserPageSkeleton() {
	return (
		<Card className="w-full max-w-md mx-auto shadow-lg">
			<CardHeader className="border-b">
				<div className="flex items-center gap-3">
					<Skeleton className="w-12 h-12 rounded-full" />
					<div className="space-y-2">
						<Skeleton className="h-6 w-40" />
						<Skeleton className="h-4 w-24" />
					</div>
				</div>
			</CardHeader>
			<CardContent className="pt-6 space-y-4">
				{[1, 2, 3, 4, 5].map((i) => (
					<div
						key={i}
						className="flex items-center justify-between p-3 rounded-lg">
						<div className="flex items-center gap-2">
							<Skeleton className="w-4 h-4 rounded" />
							<Skeleton className="h-4 w-16" />
						</div>
						<Skeleton className="h-4 w-24" />
					</div>
				))}
			</CardContent>
		</Card>
	);
}

// ============================================
// ERROR STATE COMPONENT
// ============================================
interface UserPageErrorProps {
	error: Error;
	onRetry?: () => void;
}

function UserPageError({ error, onRetry }: UserPageErrorProps) {
	return (
		<Card className="w-full max-w-md mx-auto shadow-lg border-red-200">
			<CardHeader>
				<div className="flex items-center gap-3">
					<div className="p-2 bg-red-100 rounded-full">
						<AlertCircle className="w-6 h-6 text-red-600" />
					</div>
					<CardTitle className="text-red-600">
						Something went wrong
					</CardTitle>
				</div>
				<CardDescription>
					We could not load your profile information
				</CardDescription>
			</CardHeader>

			<CardContent>
				<Alert variant="destructive" className="mb-4">
					<AlertCircle className="h-4 w-4" />
					<AlertTitle>Error</AlertTitle>
					<AlertDescription className="text-sm">
						{error.message ||
							"An unexpected error occurred. Please try again."}
					</AlertDescription>
				</Alert>

				<div className="p-4 bg-muted/50 rounded-lg text-sm text-muted-foreground">
					<p className="font-medium mb-1">Possible reasons:</p>
					<ul className="list-disc list-inside space-y-1 text-xs">
						<li>Network connection issue</li>
						<li>Authentication token expired</li>
						<li>Server is temporarily unavailable</li>
					</ul>
				</div>
			</CardContent>

			<CardFooter>
				<Button
					onClick={onRetry}
					className="w-full gap-2"
					variant="default">
					<RefreshCw className="w-4 h-4" />
					Try Again
				</Button>
			</CardFooter>
		</Card>
	);
}
