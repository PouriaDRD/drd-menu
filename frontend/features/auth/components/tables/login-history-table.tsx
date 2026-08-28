"use client";

import {
	Badge,
	Table,
	TableBody,
	TableCaption,
	TableCell,
	TableHead,
	TableHeader,
	TableRow,
} from "@/components/ui";
import { toIranDateTime } from "@/features/shared/utils";

import { useMyLoginHistory } from "../../mutations";
import type { LoginHistory } from "../../types";

/* ==========================================================================
   MAIN COMPONENT
========================================================================== */

export function LoginHistoryTable() {
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
		<div className="max-h-96 overflow-auto">
			<Table>
				<TableHeader className="sticky top-0 z-10 bg-card/85 backdrop-blur-2xl">
					<TableRow>
						<TableHead className="text-center">#</TableHead>

						<TableHead className="text-center">تاریخ</TableHead>

						<TableHead className="text-center">وضعیت</TableHead>

						<TableHead className="text-center">دستگاه</TableHead>

						<TableHead className="text-center">مرورگر</TableHead>

						<TableHead className="text-center">
							سیستم عامل
						</TableHead>

						<TableHead className="text-center">موقعیت</TableHead>

						<TableHead className="text-center">IP</TableHead>

						<TableHead className="text-center">توضیحات</TableHead>
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
	);
}

/* ==========================================================================
   ROW
========================================================================== */

function LoginHistoryRow({
	history,
	index,
}: {
	history: LoginHistory;
	index: number;
}) {
	const date = toIranDateTime(history.created_at);

	return (
		<TableRow className="text-muted-foreground">
			{/* -----------------------------------------------------------------
			    Index
			------------------------------------------------------------------ */}

			<TableCell className="text-center">{index + 1}#</TableCell>

			{/* -----------------------------------------------------------------
			    Date
			------------------------------------------------------------------ */}

			<TableCell className="text-center whitespace-nowrap">
				<div>{date.dateWithMonthName}</div>

				<div className="text-xs text-muted-foreground/70">
					{date.time}
				</div>
			</TableCell>

			{/* -----------------------------------------------------------------
			    Status
			------------------------------------------------------------------ */}

			<TableCell className="text-center">
				<Badge
					variant={history.is_successful ? "success" : "destructive"}>
					{history.is_successful ? "موفق" : "ناموفق"}
				</Badge>
			</TableCell>

			{/* -----------------------------------------------------------------
			    Device
			------------------------------------------------------------------ */}

			<TableCell className="text-center">
				<div className="font-medium text-foreground">
					{history.device ?? "-"}
				</div>

				{history.device_family && (
					<div className="text-xs text-muted-foreground/70">
						{history.device_family}
					</div>
				)}
			</TableCell>

			{/* -----------------------------------------------------------------
			    Browser
			------------------------------------------------------------------ */}

			<TableCell className="text-center">
				{history.browser ? (
					<>
						<div className="font-medium text-foreground">
							{history.browser}
						</div>

						{history.browser_version && (
							<div className="text-xs text-muted-foreground/70">
								{history.browser_version}
							</div>
						)}
					</>
				) : (
					"-"
				)}
			</TableCell>

			{/* -----------------------------------------------------------------
			    Operating System
			------------------------------------------------------------------ */}

			<TableCell className="text-center">
				{history.operating_system ? (
					<>
						<div className="font-medium text-foreground">
							{history.operating_system}
						</div>

						{history.operating_system_version && (
							<div className="text-xs text-muted-foreground/70">
								{history.operating_system_version}
							</div>
						)}
					</>
				) : (
					"-"
				)}
			</TableCell>

			{/* -----------------------------------------------------------------
			    Location
			------------------------------------------------------------------ */}

			<TableCell className="text-center">
				{history.city || history.region || history.country ? (
					<>
						<div className="font-medium text-foreground">
							{history.city ?? history.region ?? history.country}
						</div>

						{history.city &&
							(history.region || history.country) && (
								<div className="text-xs text-muted-foreground/70">
									{[history.region, history.country]
										.filter(Boolean)
										.join(" • ")}
								</div>
							)}

						{history.country_code && (
							<div className="text-xs uppercase text-muted-foreground/60">
								{history.country_code}
							</div>
						)}
					</>
				) : (
					"-"
				)}
			</TableCell>

			{/* -----------------------------------------------------------------
			    IP
			------------------------------------------------------------------ */}

			<TableCell className="text-center whitespace-nowrap">
				{history.ip_address ? (
					<code className="text-xs">{history.ip_address}</code>
				) : (
					"-"
				)}
			</TableCell>

			{/* -----------------------------------------------------------------
			    Failure Reason
			------------------------------------------------------------------ */}

			<TableCell className="max-w-40 text-center whitespace-normal wrap-break-word">
				{history.failure_reason ?? "ورود موفق"}
			</TableCell>
		</TableRow>
	);
}

/* ==========================================================================
   TABLE STATE
========================================================================== */

function TableState({ type }: { type: "loading" | "empty" | "error" }) {
	const captionMap = {
		loading: "در حال بارگذاری...",
		empty: "هیچ سابقه ورودی وجود ندارد",
		error: "خطا در بارگذاری اطلاعات",
	} as const;

	return (
		<Table>
			<TableCaption>{captionMap[type]}</TableCaption>

			<TableHeader>
				<TableRow>
					<TableHead className="text-center">#</TableHead>

					<TableHead className="text-center">تاریخ</TableHead>

					<TableHead className="text-center">وضعیت</TableHead>

					<TableHead className="text-center">دستگاه</TableHead>

					<TableHead className="text-center">مرورگر</TableHead>

					<TableHead className="text-center">سیستم عامل</TableHead>

					<TableHead className="text-center">موقعیت</TableHead>

					<TableHead className="text-center">IP</TableHead>

					<TableHead className="text-center">توضیحات</TableHead>
				</TableRow>
			</TableHeader>
		</Table>
	);
}
