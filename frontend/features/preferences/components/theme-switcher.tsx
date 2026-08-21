"use client";

import { VariantProps } from "class-variance-authority";
import { Check } from "lucide-react";

import {
	Button,
	DropdownMenu,
	DropdownMenuContent,
	DropdownMenuItem,
	DropdownMenuSeparator,
	DropdownMenuTrigger,
} from "@/components/ui";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/features/shared/utils";

import { THEMES } from "../constants";
import { useThemeSwitcher } from "../hooks";

export interface BaseSwitcherProps {
	className?: string;
	size?: VariantProps<typeof buttonVariants>["size"];
	variant?: VariantProps<typeof buttonVariants>["variant"];
}

export function ThemeSwitcher({
	className,
	size = "icon-sm",
	variant = "outline",
}: BaseSwitcherProps) {
	const { mounted, theme, setTheme } = useThemeSwitcher();

	if (!mounted) return null;

	const currentTheme =
		THEMES.find((item) => item.value === theme) ?? THEMES[0];

	const CurrentIcon = currentTheme.icon;

	return (
		<DropdownMenu dir="rtl">
			<DropdownMenuTrigger asChild>
				<Button
					variant={variant}
					size={size}
					className={cn("", className)}>
					<CurrentIcon
						className={`
							transition-transform
							duration-200
							data-[state=open]:scale-105
						`}
					/>
				</Button>
			</DropdownMenuTrigger>

			<DropdownMenuContent
				align="end"
				sideOffset={8}
				className={`
					w-48
					rounded-2xl
					border-border/70
					bg-card/95
					p-1.5
					shadow-lg
					backdrop-blur-xl
				`}>
				<div
					className={`
						px-3
						py-2.5
					`}>
					<p
						className={`
							text-[11px]
							font-medium
							text-muted-foreground
						`}>
						ظاهر برنامه
					</p>

					<p
						className={`
							mt-0.5
							text-sm
							font-bold
							text-foreground
						`}>
						انتخاب پوسته
					</p>
				</div>

				<DropdownMenuSeparator
					className={`
						mx-1
						bg-border/70
					`}
				/>

				<div
					className={`
						mt-1
						space-y-0.5
					`}>
					{THEMES.map((item) => {
						const Icon = item.icon;
						const isActive = theme === item.value;

						return (
							<DropdownMenuItem
								key={item.value}
								onClick={() => setTheme(item.value)}
								className={`
									cursor-pointer
									rounded-xl
									px-2.5
									py-2
									outline-none
									transition-colors
									${isActive ? "bg-accent text-accent-foreground" : "hover:bg-muted"}
								`}>
								<div
									className={`
										flex
										w-full
										items-center
										gap-2.5
									`}>
									<div
										className={`
											flex
											size-8
											shrink-0
											items-center
											justify-center
											rounded-lg
											transition-colors
											${isActive ? "bg-background text-primary" : "bg-muted/70 text-muted-foreground"}
										`}>
										<Icon
											className={`
												size-4
											`}
										/>
									</div>

									<span
										className={`
											flex-1
											text-xs
											${isActive ? "font-bold text-foreground" : "font-medium text-foreground"}
										`}>
										{item.label}
									</span>

									{isActive && (
										<div
											className={`
												flex
												size-5
												items-center
												justify-center
												rounded-full
												bg-primary
												text-primary-foreground
											`}>
											<Check
												className={`
													size-3
												`}
												strokeWidth={2.5}
											/>
										</div>
									)}
								</div>
							</DropdownMenuItem>
						);
					})}
				</div>
			</DropdownMenuContent>
		</DropdownMenu>
	);
}
