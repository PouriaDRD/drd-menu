import { z } from "zod";

export const updateProfileSchema = z.object({
	first_name: z.string().trim().min(2, "نام باید حداقل ۲ کاراکتر باشد"),

	last_name: z
		.string()
		.trim()
		.min(2, "نام خانوادگی باید حداقل ۲ کاراکتر باشد"),
});
