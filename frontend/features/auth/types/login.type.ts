import { z } from "zod";

import { loginSchema } from "../schemas";

import { Tokens } from "./token.type";

export type LoginFormValues = z.infer<typeof loginSchema>;

export type LoginData = Tokens & {
	user: string;
};

export type LoginResponse = LoginData;

export type LoginStoreState = LoginFormValues & {
	reset: () => void;
	set: (patch: Partial<LoginStoreState>) => void;

	_hasHydrated: boolean;
	setHasHydrated: (state: boolean) => void;
};
