"use client";

import {
	createContext,
	ReactNode,
	useCallback,
	useContext,
	useMemo,
	useState,
} from "react";

import { useMeQuery } from "../mutations";
import { User } from "../types";

interface UserContextType {
	user: User | null;
	setUser: (user: User | null) => void;
	clearUser: () => void;
	isAuthenticated: boolean;
	isLoading: boolean;
	refetchUser: ReturnType<typeof useMeQuery>["refetch"];
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
	// Holds a temporary user override.
	// `undefined` means "use the user from the query".
	// `null` means "explicitly no authenticated user".
	const [overrideUser, setOverrideUser] = useState<User | null | undefined>(
		undefined,
	);

	// Fetch the currently authenticated user.
	const { data, isLoading, refetch } = useMeQuery();

	// Extract the user only when the request succeeds.
	const queryUser = data?.success ? data.data : null;

	// Prefer the local override when it exists;
	// otherwise fall back to the server response.
	const user = overrideUser === undefined ? queryUser : overrideUser;

	// Stable setter to avoid unnecessary re-renders.
	const setUser = useCallback((user: User | null) => {
		setOverrideUser(user);
	}, []);

	// Clears the authenticated user locally.
	const clearUser = useCallback(() => {
		setOverrideUser(null);
	}, []);

	// Memoize the context value so consumers only
	// re-render when one of its dependencies changes.
	const value = useMemo(
		() => ({
			user,
			setUser,
			clearUser,
			isAuthenticated: !!user,
			isLoading,
			refetchUser: refetch,
		}),
		[user, isLoading, refetch, setUser, clearUser],
	);

	return (
		<UserContext.Provider value={value}>{children}</UserContext.Provider>
	);
}

export function useUser() {
	const context = useContext(UserContext);

	if (!context) {
		throw new Error("useUser must be used within UserProvider");
	}

	return context;
}
