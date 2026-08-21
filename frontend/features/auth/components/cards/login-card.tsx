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

import { LoginForm } from "../forms";

interface Props {
	onSuccess?: () => void;
}

export function LoginCard({ onSuccess }: Props) {
	return (
		<Card className="mx-auto max-w-full sm:max-w-xs w-full ring-0 border-0 bg-transparent shadow-none">
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
