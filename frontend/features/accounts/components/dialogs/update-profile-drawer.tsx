"use client";

import { useState } from "react";

import { VariantProps } from "class-variance-authority";
import { UserPen } from "lucide-react";

import {
	Button,
	Drawer,
	DrawerClose,
	DrawerContent,
	DrawerDescription,
	DrawerFooter,
	DrawerHeader,
	DrawerTitle,
	DrawerTrigger,
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

export function UpdateProfileDrawer(props: Props) {
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
		<Drawer open={open} onOpenChange={setOpen}>
			<DrawerTrigger asChild>
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
			</DrawerTrigger>

			<DrawerContent dir="rtl">
				<div className="mx-auto w-full max-w-md">
					<DrawerHeader className="text-right">
						<DrawerTitle>ویرایش اطلاعات حساب</DrawerTitle>
						<DrawerDescription>
							اطلاعات کاربری خود را در فرم زیر بروزرسانی کنید.
						</DrawerDescription>
					</DrawerHeader>

					<div className="max-h-[80vh] overflow-y-auto p-4 pt-0">
						<UpdateProfileForm
							initialValues={initialValues}
							onSuccess={handleSuccess}
						/>
					</div>

					<DrawerFooter className="pt-2">
						<DrawerClose asChild>
							<Button variant="outline">انصراف</Button>
						</DrawerClose>
					</DrawerFooter>
				</div>
			</DrawerContent>
		</Drawer>
	);
}
