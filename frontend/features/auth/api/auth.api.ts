/**
 * Authentication API layer
 * All HTTP calls for auth feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import { LoginFormValues, LoginHistory, LoginResponse } from "../types";

export const authApi = {
	myLoginHistory: () => {
		return apiClient.get<LoginHistory[]>(endpoints.auth.myLoginHistory);
	},

	login: (data: LoginFormValues) => {
		return apiClient.post<LoginResponse>(endpoints.auth.login, data);
	},

	logout: ({ refresh }: { refresh: string }) => {
		return apiClient.post(endpoints.auth.logout, {
			refresh,
		});
	},
};
