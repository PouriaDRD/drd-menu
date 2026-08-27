import Link from "next/link";

import { LayoutDashboard } from "lucide-react";

import { AppIcon } from "@/components/icons";
import {
	Button,
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui";

export function AlreadyLoggedIn() {
	return (
		<Card className="w-full max-w-xs gap-4 border-none shadow-none ring-0 bg-background">
			<AppIcon className="size-10 mx-auto" />
			<CardHeader className="w-full text-center">
				<CardTitle>خوش آمدید!</CardTitle>
				<CardDescription>
					شما قبلا وارد حساب خود شده‌اید
				</CardDescription>
			</CardHeader>

			<CardContent>
				<Link href="/panel/dashboard">
					<Button variant="secondary" size="lg" className="w-full">
						<LayoutDashboard className="w-4 h-4" />
						بازگشت به پنل
					</Button>
				</Link>
			</CardContent>
		</Card>
	);
}
