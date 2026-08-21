"use client";

import Link from "next/link";

import { toast } from "sonner";

import { AppIcon } from "@/components/icons";
import {
	Button,
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui";
import { ThemeSwitcher } from "@/features/preferences/components";
import { GridShape } from "@/features/shared/components";

export default function LandingPage() {
	return (
		<main
			className="relative flex min-h-dvh flex-col items-center justify-center px-6 pb-16 pt-12 text-center"
			dir="rtl">
			<GridShape />

			<Card className="w-full max-w-sm">
				<CardHeader className="flex flex-col items-center justify-center gap-2">
					<AppIcon />

					<CardTitle suppressHydrationWarning>DRD Menu</CardTitle>

					<CardDescription suppressHydrationWarning>
						به اپ مدیریت مالی خوش آمدید!
					</CardDescription>
				</CardHeader>

				<CardContent className="flex flex-col gap-3">
					<div className="flex items-center justify-between gap-2">
						<Link href="/auth/login" className="w-full">
							<Button className="w-full" variant="outline">
								ورود به سامانه
							</Button>
						</Link>

						<ThemeSwitcher />
					</div>

					<div className="grid grid-cols-2 gap-2">
						<Button
							variant="outline"
							onClick={() =>
								toast("پیام عادی", {
									description: "این یک Toast معمولی است.",
								})
							}>
							Normal
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.success("عملیات موفق", {
									description: "اطلاعات با موفقیت ذخیره شد.",
								})
							}>
							Success
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.info("اطلاع‌رسانی", {
									description: "این یک پیام اطلاعاتی است.",
								})
							}>
							Info
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.warning("هشدار", {
									description:
										"لطفاً اطلاعات واردشده را بررسی کنید.",
								})
							}>
							Warning
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.error("خطا", {
									description: "عملیات با خطا مواجه شد.",
								})
							}>
							Error
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.loading("در حال پردازش...", {
									description: "لطفاً کمی صبر کنید.",
								})
							}>
							Loading
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast.message("Message", {
									description:
										"این Toast از نوع message است.",
								})
							}>
							Message
						</Button>

						<Button
							variant="outline"
							onClick={() =>
								toast("Toast با Action", {
									description:
										"یک Action هم به این Toast اضافه شده.",
									action: {
										label: "انجام",
										onClick: () => {
											toast.success("انجام شد");
										},
									},
								})
							}>
							Action
						</Button>
					</div>
				</CardContent>
			</Card>
		</main>
	);
}
