"use client";

import { AppIcon } from "@/components/icons";
import {
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui";
import { cn } from "@/features/shared/utils";

import { LoginForm } from "../forms";

interface Props {
	className?: string;
	onSuccess?: () => void;
}

export function LoginCard({ className, onSuccess }: Props) {
	return (
		<Card
			className={cn(`mx-auto max-w-full sm:max-w-xs w-full`, className)}>
			<CardHeader className="flex flex-col items-center">
				<AppIcon className="size-11" />
				<div className="text-center">
					<CardTitle>ورود</CardTitle>
					<CardDescription>
						برای ورود، اطلاعات زیر را وارد کنید!
					</CardDescription>
				</div>
			</CardHeader>

			<CardContent>
				<LoginForm onSuccess={onSuccess} />
			</CardContent>

			<CardFooter className="flex flex-col items-center text-center text-xs text-muted-foreground gap-1">
				<span>
					با ورود در سایت، قوانین و مقررات سامانه را می‌پذیرید.
				</span>
			</CardFooter>
		</Card>
	);
}
