/**
 * User API layer
 * All HTTP calls for user feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import { User } from "../types";

export const userApi = {
	getMe: () => {
		return apiClient.get<User>(endpoints.account.me);
	},
};
