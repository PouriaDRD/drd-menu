import { z } from "zod";

export const loginSchema = z.object({
	phone_number: z
		.string()
		.min(1, "لطفا شماره موبایل را وارد کنید")
		.regex(/^09\d{9}$/, "شماره موبایل باید با 09 شروع شود و 11 رقم باشد"),

	password: z.string().min(1, "رمز عبور باید حداقل 1 کاراکتر باشد"),
});
