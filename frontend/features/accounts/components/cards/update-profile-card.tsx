"use client";

import Link from "next/link";

import { AppIcon } from "@/components/icons";
import {
	Button,
	Card,
	CardContent,
	CardDescription,
	CardFooter,
	CardHeader,
	CardTitle,
} from "@/components/ui";
import { cn } from "@/features/shared/utils";

import { UpdateProfileForm } from "../forms";

interface Props {
	className?: string;
	onSuccess?: () => void;
}

export function UpdateProfileCard({ className, onSuccess }: Props) {
	return (
		<Card
			className={cn(
				// "mx-auto max-w-full sm:max-w-xs w-full ring-0 border-0 bg-transparent shadow-none",
				"mx-auto max-w-full sm:max-w-xs w-full",
				className,
			)}>
			<CardHeader className="flex flex-col items-center">
				<AppIcon className="size-11" />
				<div className="text-center">
					<CardTitle>ویرایش اطلاعات</CardTitle>
					<CardDescription>اطلاعات خود را بروز کنید!</CardDescription>
				</div>
			</CardHeader>

			<CardContent>
				<UpdateProfileForm onSuccess={onSuccess} />
			</CardContent>

			<CardFooter className="flex flex-col items-center text-center text-xs text-muted-foreground gap-1">
				<Link href="/auth/register">
					حساب کاربری ندارید؟
					<Button variant={"link"} size={"xs"}>
						ثبت نام کنید
					</Button>
				</Link>
				<span>
					با ورود در سایت، قوانین و مقررات سامانه را می‌پذیرید.
				</span>
			</CardFooter>
		</Card>
	);
}
