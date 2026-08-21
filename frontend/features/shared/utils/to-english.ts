export function toEnglishDigits(value: string): string {
	const persian = "۰۱۲۳۴۵۶۷۸۹";
	const arabic = "٠١٢٣٤٥٦٧٨٩";

	return value
		.replace(/[۰-۹]/g, (d) => persian.indexOf(d).toString())
		.replace(/[٠-٩]/g, (d) => arabic.indexOf(d).toString());
}

export function normalizeToEnglish(input: string) {
	return input
		.replace(/[۰-۹]/g, (d) => "۰۱۲۳۴۵۶۷۸۹".indexOf(d).toString())
		.replace(/\s+/g, "")
		.trim();
}
