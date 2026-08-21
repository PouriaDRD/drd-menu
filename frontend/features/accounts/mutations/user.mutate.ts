"use client";

import { useMutation, useQuery } from "@tanstack/react-query";

import { queryKeys } from "@/features/api/lib";

import { userApi } from "../api";

export function useMeQuery() {
	return useQuery({
		queryKey: queryKeys.accounts.myProfile,
		queryFn: userApi.getMe,
		// auto refresh every 120 seconds
		refetchInterval: 120 * 1000,
	});
}

export function useUpdateProfile() {
	return useMutation({
		mutationFn: userApi.updateProfile,
	});
}
