import { z } from "zod";

import { registerSchema } from "../schemas";

import { Tokens } from "./token.type";

export type RegisterFormValues = z.infer<typeof registerSchema>;

export type RegisterData = Tokens & {
	user: string;
};

export type RegisterResponse = RegisterData;

export type RegisterStoreState = RegisterFormValues & {
	reset: () => void;
	set: (patch: Partial<RegisterStoreState>) => void;

	_hasHydrated: boolean;
	setHasHydrated: (state: boolean) => void;
};
