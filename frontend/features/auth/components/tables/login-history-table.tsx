"use client";

import {
	CalendarDays,
	Globe,
	Laptop,
	LogIn,
	MonitorSmartphone,
	ShieldCheck,
	Text,
} from "lucide-react";

import {
	Badge,
	Card,
	CardHeader,
	CardTitle,
	Table,
	TableBody,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui";
import { cn, toIranDateTime } from "@/features/shared/utils";

import { useMyLoginHistory } from "../../mutations";
import { LoginHistory } from "../../types";

/* =========================================================
   MAIN COMPONENT
========================================================= */

export function LoginHistoryCardTable() {
	return (
		<Card className="overflow-hidden gap-0">
			<CardHeader className="flex flex-row items-center justify-between border-b bg-card/80 backdrop-blur-xl">
				<div className="flex items-center gap-3">
					<div className="flex size-9 shrink-0 items-center justify-center rounded-lg border bg-muted/40 text-muted-foreground">
						<LogIn className="size-4" strokeWidth={1.8} />
					</div>

					<div className="space-y-0.5">
						<CardTitle
							className="text-base"
							suppressHydrationWarning>
							تاریخچه ورود
						</CardTitle>

						<p className="text-xs text-muted-foreground">
							سوابق ورود به حساب کاربری شما
						</p>
					</div>
				</div>
			</CardHeader>

			<LoginHistoryTable />
		</Card>
	);
}

/* =========================================================
   TABLE
========================================================= */

function LoginHistoryTable() {
	const { data, isLoading, isError } = useMyLoginHistory();

	if (isLoading) {
		return <TableState type="loading" />;
	}

	if (isError || !data?.success) {
		return <TableState type="error" />;
	}

	const histories = data.data ?? [];

	if (histories.length === 0) {
		return <TableState type="empty" />;
	}

	return (
		<div className="overflow-hidden">
			<div className="flex max-h-96 overflow-auto">
				<Table>
					<TableHeader className="sticky top-0 z-20 bg-card/95 backdrop-blur-xl">
						<TableRow>
							{/* INDEX */}
							<TableHead className="w-12 px-3 text-center text-[11px] font-medium text-muted-foreground">
								#
							</TableHead>

							{/* DATE */}
							<TableHead className="min-w-36 px-3 text-center text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel
									icon={CalendarDays}
									label="تاریخ"
								/>
							</TableHead>

							{/* STATUS */}
							<TableHead className="px-3 text-center text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel
									icon={ShieldCheck}
									label="وضعیت"
								/>
							</TableHead>

							{/* DEVICE */}
							<TableHead className="min-w-32 px-3 text-center text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel
									icon={MonitorSmartphone}
									label="دستگاه"
								/>
							</TableHead>

							{/* BROWSER */}
							<TableHead className="min-w-32 px-3 text-center text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel icon={Globe} label="مرورگر" />
							</TableHead>

							{/* IP */}
							<TableHead className="min-w-32 px-3 text-center text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel icon={Laptop} label="IP" />
							</TableHead>

							{/* DESCRIPTION */}
							<TableHead className="min-w-48 px-3 text-right text-[11px] font-medium text-muted-foreground">
								<TableHeaderLabel icon={Text} label="توضیحات" />
							</TableHead>
						</TableRow>
					</TableHeader>

					<TableBody>
						{histories.map((history, index) => (
							<LoginHistoryRow
								key={history.id}
								history={history}
								index={index}
							/>
						))}
					</TableBody>
				</Table>
			</div>
		</div>
	);
}

/* =========================================================
   TABLE HEADER LABEL
========================================================= */

function TableHeaderLabel({
	icon: Icon,
	label,
}: {
	icon: typeof CalendarDays;
	label: string;
}) {
	return (
		<div className="inline-flex items-center justify-center gap-1.5">
			<Icon
				className="size-3.5 text-muted-foreground/70"
				strokeWidth={1.8}
			/>

			<span>{label}</span>
		</div>
	);
}

/* =========================================================
   ROW
========================================================= */

function LoginHistoryRow({
	history,
	index,
}: {
	history: LoginHistory;
	index: number;
}) {
	const date = toIranDateTime(history.created_at);

	const isSuccessful = history.is_successful;

	return (
		<TableRow
			className={cn(
				"group border-b transition-colors last:border-0",
				"hover:bg-muted/20",
			)}>
			{/* INDEX */}
			<TableCell
				className="px-3 text-center text-xs tabular-nums text-muted-foreground/60"
				suppressHydrationWarning>
				{index + 1}
			</TableCell>

			{/* DATE */}
			<TableCell className="px-3 text-center" suppressHydrationWarning>
				<div className="space-y-0.5">
					<div className="text-xs font-medium">
						{date.dateWithMonthName}
					</div>

					<div className="text-[10px] tabular-nums text-muted-foreground">
						{date.time}
					</div>
				</div>
			</TableCell>

			{/* STATUS */}
			<TableCell className="px-3 text-center" suppressHydrationWarning>
				<LoginStatusBadge isSuccessful={isSuccessful} />
			</TableCell>

			{/* DEVICE */}
			<TableCell
				className="max-w-40 px-3 text-center"
				suppressHydrationWarning>
				<div className="flex items-center justify-center gap-2">
					<MonitorSmartphone className="size-3.5 shrink-0 text-muted-foreground/60" />

					<span className="truncate text-xs text-muted-foreground">
						{history.device ?? "نامشخص"}
					</span>
				</div>
			</TableCell>

			{/* BROWSER */}
			<TableCell
				className="max-w-40 px-3 text-center"
				suppressHydrationWarning>
				<div className="flex items-center justify-center gap-2">
					<Globe className="size-3.5 shrink-0 text-muted-foreground/60" />

					<span className="truncate text-xs text-muted-foreground">
						{history.browser ?? "نامشخص"}
					</span>
				</div>
			</TableCell>

			{/* IP */}
			<TableCell className="px-3 text-center" suppressHydrationWarning>
				<code className="rounded-md bg-muted/50 px-2 py-1 text-[11px] tabular-nums text-muted-foreground">
					{history.ip_address ?? "-"}
				</code>
			</TableCell>

			{/* DESCRIPTION */}
			<TableCell
				className="max-w-64 px-3 text-right"
				suppressHydrationWarning>
				<p
					className={cn(
						"truncate text-xs",
						isSuccessful
							? "text-muted-foreground"
							: "text-rose-600 dark:text-rose-400",
					)}>
					{history.failure_reason ?? "ورود موفق"}
				</p>
			</TableCell>
		</TableRow>
	);
}

/* =========================================================
   STATUS BADGE
========================================================= */

function LoginStatusBadge({ isSuccessful }: { isSuccessful: boolean }) {
	return (
		<Badge
			variant="outline"
			className={cn(
				"gap-1.5 border px-2 py-0.5 text-[11px] font-medium",
				isSuccessful
					? "border-emerald-500/20 bg-emerald-500/5 text-emerald-600 dark:text-emerald-400"
					: "border-rose-500/20 bg-rose-500/5 text-rose-600 dark:text-rose-400",
			)}>
			<span
				className={cn(
					"size-1.5 rounded-full",
					isSuccessful ? "bg-emerald-500" : "bg-rose-500",
				)}
			/>

			{isSuccessful ? "موفق" : "ناموفق"}
		</Badge>
	);
}

/* =========================================================
   STATES
========================================================= */

function TableState({ type }: { type: "loading" | "empty" | "error" }) {
	const content = {
		loading: {
			title: "در حال بارگذاری",
			description: "لطفاً کمی صبر کنید...",
		},

		empty: {
			title: "سابقه‌ای وجود ندارد",
			description: "هنوز هیچ سابقه‌ای از ورود به حساب شما ثبت نشده است.",
		},

		error: {
			title: "خطا در دریافت اطلاعات",
			description: "دریافت تاریخچه ورود با مشکل مواجه شد.",
		},
	}[type];

	return (
		<div className="flex min-h-52 items-center justify-center">
			<div className="text-center">
				<div className="mx-auto mb-3 flex size-8 items-center justify-center rounded-lg bg-muted">
					{type === "loading" ? (
						<div className="size-3.5 animate-spin rounded-full border-2 border-muted-foreground/30 border-t-foreground" />
					) : (
						<span className="text-xs font-semibold text-muted-foreground">
							{type === "empty" ? "—" : "!"}
						</span>
					)}
				</div>

				<h3 className="text-sm font-medium">{content.title}</h3>

				<p className="mt-1 text-xs text-muted-foreground">
					{content.description}
				</p>
			</div>
		</div>
	);
}
