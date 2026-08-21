import { useMutation, useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/features/api/lib";

import { authApi } from "../api";

export function useLogin() {
	return useMutation({
		mutationFn: authApi.login,
	});
}

export function useLogoutMutation() {
	return useMutation({
		mutationFn: authApi.logout,
	});
}

export const useMyLoginHistory = () => {
	return useQuery({
		queryKey: queryKeys.auth.myLoginHistory,
		queryFn: authApi.myLoginHistory,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
};
