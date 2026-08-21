"use client";

import {
	BadgeCheck,
	CalendarDays,
	Phone,
	Shield,
	User as UserIcon,
} from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { User } from "@/features/accounts/types";
import { toIranDateTime } from "@/features/shared/utils";

interface UserCardProps {
	user: User;
}

export function SimpleUserCard({ user }: UserCardProps) {
	const roleIcon = {
		superuser: <Shield className="w-4 h-4 text-purple-600" />,
		admin: <BadgeCheck className="w-4 h-4 text-blue-600" />,
		user: <UserIcon className="w-4 h-4 text-gray-600" />,
	}[user.role];

	const lastLogin = toIranDateTime(user.last_login);
	const createdAt = toIranDateTime(user.created_at);

	return (
		<Card className="w-full max-w-xs">
			<CardHeader className="border-b">
				<CardTitle className="text-2xl font-bold flex items-center gap-3">
					<div className="p-2 bg-primary/10 rounded-full">
						<UserIcon className="w-6 h-6 text-primary" />
					</div>
					<span>{user.full_name}</span>
				</CardTitle>
			</CardHeader>

			<CardContent className="pt-6 space-y-4">
				{/* Role */}
				<div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
					<div className="flex items-center gap-2 text-muted-foreground">
						{roleIcon}
						<span className="font-medium">Role</span>
					</div>
					<span className="capitalize font-semibold">
						{user.role}
					</span>
				</div>

				{/* Phone */}
				<div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
					<div className="flex items-center gap-2 text-muted-foreground">
						<Phone className="w-4 h-4" />
						<span className="font-medium">Phone</span>
					</div>
					<span dir="ltr">{user.phone_number}</span>
				</div>

				{/* Last Login */}
				<div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
					<div className="flex items-center gap-2 text-muted-foreground">
						<CalendarDays className="w-4 h-4" />
						<span className="font-medium">Last Login</span>
					</div>
					<span className="text-sm">
						{lastLogin.dateWithMonthName} {lastLogin.time}
					</span>
				</div>

				{/* Joined */}
				<div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
					<div className="flex items-center gap-2 text-muted-foreground">
						<CalendarDays className="w-4 h-4" />
						<span className="font-medium">Joined</span>
					</div>
					<span className="text-sm">
						{createdAt.dateWithMonthName} {createdAt.time}
					</span>
				</div>
			</CardContent>
		</Card>
	);
}
