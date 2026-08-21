/**
 * Authentication API layer
 * All HTTP calls for auth feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import {
	LoginFormValues,
	LoginHistory,
	LoginResponse,
	RegisterFormValues,
	RegisterResponse,
} from "../types";

export const authApi = {
	myLoginHistory: () => {
		return apiClient.get<LoginHistory[]>(endpoints.auth.myLoginHistory);
	},

	login: (data: LoginFormValues) => {
		return apiClient.post<LoginResponse>(endpoints.auth.login, data);
	},

	register: (data: RegisterFormValues) => {
		return apiClient.post<RegisterResponse>(endpoints.auth.register, data);
	},
};
