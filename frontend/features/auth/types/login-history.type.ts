export type LoginHistory = {
	id: string;

	ip_address?: string | null;

	user_agent?: string | null;

	device?: string | null;

	browser?: string | null;

	operating_system?: string | null;

	country?: string | null;

	city?: string | null;

	is_successful: boolean;

	failure_reason?: string | null;

	created_at: Date;
};
