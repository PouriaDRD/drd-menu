"use client";

import { VariantProps } from "class-variance-authority";
import { LogOut } from "lucide-react";

import {
	AlertDialog,
	AlertDialogAction,
	AlertDialogCancel,
	AlertDialogContent,
	AlertDialogDescription,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogTitle,
	AlertDialogTrigger,
	Button,
	Spinner,
} from "@/components/ui";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/features/shared/utils";

import { useLogout } from "../../hooks";

interface Props {
	collapsed?: boolean;
	className?: string;
	size?: VariantProps<typeof buttonVariants>["size"];
	variant?: VariantProps<typeof buttonVariants>["variant"];
}

export function LogoutDialog(props: Props) {
	const {
		className,
		size = "default",
		variant = "outline",
		collapsed = false,
	} = props;

	const { handleLogout, isLoading } = useLogout();

	return (
		<AlertDialog>
			<AlertDialogTrigger asChild>
				<Button
					size={size}
					variant={variant}
					className={cn(
						`${collapsed ? "size-10 p-0" : ""}`,
						className,
					)}>
					{isLoading ? (
						<Spinner className="size-4 shrink-0 text-destructive" />
					) : (
						<LogOut className="size-4 shrink-0 text-destructive" />
					)}
					{!collapsed && (
						<span className="text-destructive">
							{isLoading ? "در حال خروج از حساب" : "خروج از حساب"}
						</span>
					)}
				</Button>
			</AlertDialogTrigger>

			<AlertDialogContent dir="rtl">
				<AlertDialogHeader>
					<AlertDialogTitle>خروج از حساب کاربری</AlertDialogTitle>

					<AlertDialogDescription>
						آیا مطمئن هستید که می‌خواهید از حساب کاربری خود خارج
						شوید؟
					</AlertDialogDescription>
				</AlertDialogHeader>

				<AlertDialogFooter className="flex-col">
					<AlertDialogCancel>انصراف</AlertDialogCancel>

					<AlertDialogAction
						variant={"destructive"}
						onClick={handleLogout}>
						خروج
					</AlertDialogAction>
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
}
