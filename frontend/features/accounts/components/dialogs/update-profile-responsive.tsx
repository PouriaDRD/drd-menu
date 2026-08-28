"use client";

import { ComponentProps } from "react";

import { useIsMobile } from "@/features/shared/hooks";

import { UpdateProfileDialog } from "./update-profile-dialog";
import { UpdateProfileDrawer } from "./update-profile-drawer";

type Props = ComponentProps<typeof UpdateProfileDialog>;

export function UpdateProfileResponsive(props: Props) {
	const isMobile = useIsMobile();

	// Render Drawer for Mobile screens, Dialog for Desktop screens
	if (isMobile) {
		return <UpdateProfileDrawer {...props} />;
	}

	return <UpdateProfileDialog {...props} />;
}
