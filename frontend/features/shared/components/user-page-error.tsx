"use client";

import { RefreshCw } from "lucide-react";

import { AppIcon } from "@/components/icons";
import { PageLayout } from "@/components/layouts";
import {
	Button,
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui";

import { GridShape } from "./grid-shape";

interface Props {
	error: Error;
	onRetry?: () => void;
}

export function UserPageError({ error, onRetry }: Props) {
	if (process.env.NODE_ENV === "development") {
		console.error(error);
	}

	return (
		<PageLayout className="flex items-center justify-center h-dvh w-full">
			<GridShape />
			<Card className="w-full max-w-xs border-none shadow-none ring-0 bg-background">
				<AppIcon className="size-10 mx-auto" />
				<CardHeader className="w-full text-center">
					<CardTitle>خطا در دریافت اطلاعات</CardTitle>
					<CardDescription>
						امکان بارگذاری اطلاعات پروفایل شما وجود ندارد
					</CardDescription>
				</CardHeader>

				<CardContent className="space-y-4">
					{/* <Alert variant="destructive">
						<AlertCircle className="size-4" />
						<AlertTitle>خطا</AlertTitle>
						<AlertDescription className="text-sm">
							{error.message ||
								"خطایی غیرمنتظره رخ داده است. لطفاً دوباره تلاش کنید."}
						</AlertDescription>
					</Alert> */}

					<div>
						<p className="font-medium mb-1">دلایل احتمالی:</p>
						<ul className="list-disc list-inside space-y-1 text-xs">
							<li>مشکل در اتصال به شبکه</li>
							<li>انقضای نشست کاربری (توکن)</li>
							<li>عدم دسترس‌پذیری موقت سرور</li>
						</ul>
					</div>
				</CardContent>

				<CardFooter>
					<Button
						onClick={onRetry}
						className="w-full gap-2"
						variant="default">
						<RefreshCw className="size-4" />
						تلاش مجدد
					</Button>
				</CardFooter>
			</Card>
		</PageLayout>
	);
}
