"use client";

import {
	BadgeCheck,
	CalendarDays,
	Clock,
	Phone,
	Shield,
	User as UserIcon,
} from "lucide-react";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Card, CardContent } from "@/components/ui/card";
import { User, UserRole } from "@/features/accounts/types";
import { toIranDateTime } from "@/features/shared/utils";

interface SimpleUserCardProps {
	user: User;
}

export function SimpleUserCard({ user }: SimpleUserCardProps) {
	const roleInfo = roleConfig[user.role] ?? roleConfig.user;
	const lastLogin = toIranDateTime(user.last_login);
	const createdAt = toIranDateTime(user.created_at);

	const userInitials =
		user.first_name && user.last_name
			? `${user.first_name[0]}${user.last_name[0]}`
			: user.full_name?.slice(0, 2) || "ک";

	return (
		<Card className="overflow-hidden border-border/60 shadow-sm" dir="rtl">
			{/* Minimal Header Section */}
			<div className="relative flex flex-col items-center px-6 pb-6 pt-8 text-center">
				{/* Avatar with dynamic Status Indicator Ring */}
				<div className="relative">
					<Avatar className="h-20 w-20 border-2 border-background shadow-md">
						<AvatarFallback className="bg-primary/10 text-xl font-bold text-primary">
							{userInitials}
						</AvatarFallback>
					</Avatar>
				</div>

				{/* User Name */}
				<h2 className="mt-4 text-lg font-bold tracking-tight text-foreground">
					{user.full_name}
				</h2>

				{/* Minimal Inline Role Display (No Badge) */}
				<div className="mt-1.5 flex items-center gap-1.5 text-xs text-muted-foreground">
					{roleInfo.icon}
					<span className="font-medium">{roleInfo.label}</span>
				</div>
			</div>

			{/* Content List */}
			<CardContent className="space-y-1 p-3 pt-0">
				{/* Phone Number */}
				<div className="flex items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-colors hover:bg-muted/50">
					<div className="flex items-center gap-2.5 text-muted-foreground">
						<Phone className="h-4 w-4 shrink-0 stroke-[1.75]" />
						<span className="text-xs font-medium">شماره همراه</span>
					</div>
					<span
						dir="ltr"
						className="font-mono text-xs font-semibold text-foreground">
						{user.phone_number}
					</span>
				</div>

				{/* Last Login At */}
				<div className="flex items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-colors hover:bg-muted/50">
					<div className="flex items-center gap-2.5 text-muted-foreground">
						<Clock className="h-4 w-4 shrink-0 stroke-[1.75]" />
						<span className="text-xs font-medium">آخرین ورود</span>
					</div>
					<span className="text-xs text-foreground/80">
						{lastLogin.dateWithMonthName}{" "}
						<span className="text-muted-foreground/50">•</span>{" "}
						{lastLogin.time}
					</span>
				</div>

				{/* Joined At */}
				<div className="flex items-center justify-between rounded-lg px-3 py-2.5 text-sm transition-colors hover:bg-muted/50">
					<div className="flex items-center gap-2.5 text-muted-foreground">
						<CalendarDays className="h-4 w-4 shrink-0 stroke-[1.75]" />
						<span className="text-xs font-medium">تاریخ عضویت</span>
					</div>
					<span className="text-xs text-foreground/80">
						{createdAt.dateWithMonthName}{" "}
						<span className="text-muted-foreground/50">•</span>{" "}
						{createdAt.time}
					</span>
				</div>
			</CardContent>
		</Card>
	);
}

const roleConfig: Record<
	UserRole,
	{
		label: string;
		icon: React.ReactNode;
		indicatorColor: string;
	}
> = {
	superuser: {
		label: "مدیر ارشد",
		icon: (
			<Shield className="h-3.5 w-3.5 text-purple-600 dark:text-purple-400" />
		),
		indicatorColor: "bg-purple-500",
	},
	admin: {
		label: "مدیر سیستم",
		icon: (
			<BadgeCheck className="h-3.5 w-3.5 text-blue-600 dark:text-blue-400" />
		),
		indicatorColor: "bg-blue-500",
	},
	user: {
		label: "کاربر عادی",
		icon: <UserIcon className="h-3.5 w-3.5 text-muted-foreground" />,
		indicatorColor: "bg-emerald-500",
	},
};
