/**
 * User API layer
 * All HTTP calls for user feature
 */

import { apiClient, endpoints } from "@/features/api/lib";

import { User } from "../types";
import { ProfileFormValues } from "../types/update-profile.types";

export const userApi = {
	getMe: () => {
		return apiClient.get<User>(endpoints.account.myProfile);
	},

	updateProfile: (data: ProfileFormValues) => {
		return apiClient.patch<ProfileFormValues>(
			endpoints.account.updateProfile,
			data,
		);
	},
};
