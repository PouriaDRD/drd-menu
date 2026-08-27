import { AppIcon } from "@/components/icons";
import { PageLayout } from "@/components/layouts";
import {
	Card,
	CardDescription,
	CardHeader,
	CardTitle,
	Spinner,
} from "@/components/ui";

import { GridShape } from "./grid-shape";

const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME;

export function LoadingCard() {
	return (
		<PageLayout className="flex items-center justify-center h-dvh w-full">
			<GridShape />
			<Card className="w-full max-w-xs gap-4 border-none shadow-none ring-0 bg-background">
				<AppIcon className="size-10 mx-auto" />
				<CardHeader className="w-full text-center">
					<CardTitle>{APP_NAME}</CardTitle>
					<CardDescription className="flex items-center justify-center gap-1 w-full">
						در حال بارگذاری
						<Spinner />
					</CardDescription>
				</CardHeader>
			</Card>
		</PageLayout>
	);
}
