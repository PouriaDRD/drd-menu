export type UserRole = "superuser" | "admin" | "user";

export type UserStatus = "active" | "inactive" | "banned";

export type User = {
	id: string;
	first_name: string;
	last_name: string;
	full_name: string;
	phone_number: string;
	role: UserRole;
	status: UserStatus;
	last_login: Date;
	created_at: Date;
};
