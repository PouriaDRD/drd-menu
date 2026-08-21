"use client";

import { useEffect } from "react";

import Link from "next/link";

import { Home, RotateCcw, TriangleAlert } from "lucide-react";

import { Button } from "@/components/ui";
import { GridShape } from "@/features/shared/components";

interface Props {
	error: Error & { digest?: string };
	reset: () => void;
}

export default function Error({ error, reset }: Props) {
	useEffect(() => {
		// Log to your error monitoring (Sentry, etc.)
		if (process.env.NODE_ENV === "development") {
			console.error(error);
		}
	}, [error]);

	return (
		<main
			className={`flex min-h-dvh flex-col items-center 
			justify-center px-6 pb-16 pt-12 text-center`}
			dir="rtl">
			<GridShape />
			{/* Icon */}
			<div className="mb-5 flex size-14 items-center justify-center rounded-2xl bg-primary/5 dark:bg-primary">
				<TriangleAlert
					className="size-7 text-primary dark:text-foreground"
					strokeWidth={1.75}
				/>
			</div>

			{/* Label */}
			<p className="mb-2 text-[10px] font-bold uppercase tracking-[1.5px] text-primary">
				خطای سرور
			</p>

			<h1 className="text-[20px] font-black tracking-tight text-foreground">
				مشکلی پیش اومد
			</h1>

			<p className="mt-2 max-w-60 text-[13px] font-light leading-relaxed text-muted-foreground">
				یه خطای غیرمنتظره رخ داده. تیم ما در حال بررسیه.
			</p>

			{/* Actions */}
			<div className="mt-8 flex  flex-col gap-3">
				<Button variant={"default"} onClick={reset}>
					<RotateCcw className="size-3.5" />
					تلاش دوباره
				</Button>

				<Link href="/" className="w-full">
					<Button variant={"outline"} className="w-full">
						<Home className="size-3.5" />
						برگشت به خانه
					</Button>
				</Link>
			</div>
		</main>
	);
}
