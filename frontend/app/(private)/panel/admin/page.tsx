import { UpdateProfileCard } from "@/features/accounts/components/cards";
import { GridShape } from "@/features/shared/components";

export default function AdminPage() {
	return (
		<main
			className={`relative flex min-h-dvh flex-col items-center
				justify-center text-center gap-4`}>
			<GridShape />

			<UpdateProfileCard />
		</main>
	);
}
