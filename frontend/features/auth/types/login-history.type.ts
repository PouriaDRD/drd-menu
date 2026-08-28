export type LoginHistoryDevice = "PC" | "Mobile" | "Tablet" | "Bot" | "Unknown";

export type LoginHistory = {
	id: string;

	user: string;

	is_successful: boolean;
	failure_reason: string | null;

	ip_address: string | null;

	user_agent: string | null;

	device: LoginHistoryDevice | null;
	device_family: string | null;

	browser: string | null;
	browser_version: string | null;

	operating_system: string | null;
	operating_system_version: string | null;

	country: string | null;
	country_code: string | null;
	region: string | null;
	city: string | null;

	latitude: number | null;
	longitude: number | null;

	created_at: string;
	updated_at: string;
};
