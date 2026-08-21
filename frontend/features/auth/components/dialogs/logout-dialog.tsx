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

import { useLogout } from "../../hooks";

interface Props {
	collapsed: boolean;
}

export function LogoutDialog({ collapsed }: Props) {
	const { handleLogout, isLoading } = useLogout();

	return (
		<AlertDialog>
			<AlertDialogTrigger>
				<Button
					variant="ghost"
					className={collapsed ? "size-10 p-0" : "justify-start"}>
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
						onClick={handleLogout}
						className="bg-destructive hover:bg-destructive/90">
						خروج
					</AlertDialogAction>
				</AlertDialogFooter>
			</AlertDialogContent>
		</AlertDialog>
	);
}
