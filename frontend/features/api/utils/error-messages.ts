import { ApiErrorCode } from "../types";

const ERROR_MESSAGES: Record<ApiErrorCode, string> = {
	SUCCESS: "عملیات موفق بود.",

	// Authentication
	PERMISSION_DENIED: "شما دسترسی ندارید.",
	NOT_AUTHENTICATED: "لطفا ابتدا وارد حساب خود شوید.",
	AUTHENTICATION_ERROR: "لطفا ابتدا وارد حساب خود شوید.",

	ACCOUNT_NOT_FOUND: "حساب کاربری یافت نشد.",
	ACCOUNT_DISABLED: "حساب کاربری غیرفعال شده است.",

	// Server
	NOT_FOUND: "اطلاعات پیدا نشد.",
	SERVER_ERROR: "خطای سرور رخ داده است.",
	REQUEST_TIMEOUT: "زمان درخواست تمام شد.",
	NETWORK_ERROR: "ارتباط با سرور برقرار نشد.",
	THROTTLED: "تعداد درخواست‌ها زیاد است، کمی بعد تلاش کنید.",

	// Validation
	VALIDATION_ERROR: "اطلاعات وارد شده صحیح نیست.",

	INVALID_CREDENTIALS: "اطلاعات وارد شده صحیح نیست.",
	INVALID_PHONE_NUMBER: "شماره موبایل صحیح نیست.",

	FIRST_NAME_TOO_SHORT: "نام باید حداقل ۳ کاراکتر باشد.",
	LAST_NAME_TOO_SHORT: "نام خانوادگی باید حداقل ۳ کاراکتر باشد.",

	EMAIL_ALREADY_EXISTS: "این ایمیل قبلا ثبت شده است.",
	PHONE_ALREADY_EXISTS: "این شماره موبایل قبلا ثبت شده است.",
	USERNAME_ALREADY_EXISTS: "نام کاربری قبلا ثبت شده است.",
};

export function getApiErrorMessage(code?: ApiErrorCode) {
	if (!code) return "خطایی رخ داده است.";

	return ERROR_MESSAGES[code];
}
