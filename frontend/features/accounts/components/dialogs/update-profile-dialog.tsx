"use client";

import { useState } from "react";

import { VariantProps } from "class-variance-authority";
import { UserPen } from "lucide-react";

import {
	Button,
	Dialog,
	DialogContent,
	DialogDescription,
	DialogHeader,
	DialogTitle,
	DialogTrigger,
} from "@/components/ui";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/features/shared/utils";

import { ProfileFormValues } from "../../types";
import { UpdateProfileForm } from "../forms";

interface Props {
	initialValues?: ProfileFormValues;
	collapsed?: boolean;
	className?: string;
	size?: VariantProps<typeof buttonVariants>["size"];
	variant?: VariantProps<typeof buttonVariants>["variant"];
	onSuccess?: () => void;
}

export function UpdateProfileDialog(props: Props) {
	const {
		initialValues,
		className,
		size = "default",
		variant = "outline",
		collapsed = false,
		onSuccess,
	} = props;

	const [open, setOpen] = useState(false);

	// Close state and invoke optional parent callback on submit
	const handleSuccess = () => {
		setOpen(false);
		onSuccess?.();
	};

	return (
		<Dialog open={open} onOpenChange={setOpen}>
			<DialogTrigger asChild>
				<Button
					size={size}
					variant={variant}
					className={cn(
						`${collapsed ? "size-10 p-0" : ""}`,
						className,
					)}>
					<UserPen className="size-4 shrink-0" />
					{!collapsed && <span>ویرایش اطلاعات</span>}
				</Button>
			</DialogTrigger>

			<DialogContent dir="rtl" className="sm:max-w-sm">
				<DialogHeader className="text-right">
					<DialogTitle>ویرایش اطلاعات حساب</DialogTitle>
					<DialogDescription>
						اطلاعات کاربری خود را در فرم زیر بروزرسانی کنید.
					</DialogDescription>
				</DialogHeader>

				<div className="max-h-[70vh] overflow-y-auto px-1 py-2">
					<UpdateProfileForm
						initialValues={initialValues}
						onSuccess={handleSuccess}
					/>
				</div>
			</DialogContent>
		</Dialog>
	);
}
