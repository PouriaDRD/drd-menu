"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

import { RegisterStoreState } from "../types/register.type";

export const useRegisterStore = create<RegisterStoreState>()(
	persist(
		(set) => ({
			email: "",
			name: "",
			password: "",
			confirm_password: "",

			set: (patch) => set((state) => ({ ...state, ...patch })),

			reset: () =>
				set({
					email: "",
					name: "",
					password: "",
					confirm_password: "",
				}),

			_hasHydrated: false,
			setHasHydrated: (state: boolean) => set({ _hasHydrated: state }),
		}),
		{
			name: "rgs-store",

			// Store in Browser's localStorage only if browser is available
			storage: createJSONStorage(() => {
				if (typeof window !== "undefined") {
					return localStorage;
				}
				return {
					getItem: () => null,
					setItem: () => {},
					removeItem: () => {},
				};
			}),

			// Only save these states to storage (Not Password)
			partialize: (state) => ({
				email: state.email,
				name: state.name,
			}),
			onRehydrateStorage: () => (state) => {
				state?.setHasHydrated(true);
			},
		},
	),
);
