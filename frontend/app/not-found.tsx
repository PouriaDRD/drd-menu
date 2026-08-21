import Link from "next/link";

import { ArrowRight } from "lucide-react";

import { Button } from "@/components/ui";
import { GridShape } from "@/features/shared/components";

export default function NotFound() {
	return (
		<main
			className={`relative flex min-h-dvh flex-col items-center 
			justify-center px-6 pb-16 pt-12 text-center`}
			dir="rtl">
			<GridShape />
			{/* Big 404 with accent zero */}
			<div
				suppressHydrationWarning
				aria-hidden="true"
				className="select-none text-[96px] font-black leading-none tracking-[-6px] text-foreground">
				۴<span className="text-primary">۰</span>۴
			</div>

			<h1
				suppressHydrationWarning
				className="mt-5 text-[18px] font-bold tracking-tight text-foreground">
				صفحه پیدا نشد
			</h1>

			<p
				suppressHydrationWarning
				className="mt-2 max-w-60 text-[13px] font-light leading-relaxed text-muted-foreground">
				صفحه‌ای که دنبالش می‌گردی وجود نداره یا جابه‌جا شده.
			</p>

			{/* Actions */}
			<div className="mt-8 flex w-full max-w-55 flex-col gap-3">
				<Link href="/">
					<Button variant={"outline"}>
						<ArrowRight className="size-3.5" />
						برگشت به خانه
					</Button>
				</Link>
			</div>
		</main>
	);
}
