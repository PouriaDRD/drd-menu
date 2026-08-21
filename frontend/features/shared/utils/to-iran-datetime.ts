import { toEnglishDigits } from "./to-english";

interface DateTime {
	date: string;
	time: string;
	datetime: string;
	monthName: string;
	dateWithMonthName: string;
	datetimeWithMonthName: string;
	year: number;
	month: number;
	day: number;
	hour: number;
	minute: number;
}

/**
 * Convert UTC date to Iranian (Jalali) date/time
 */
export function toIranDateTime(date: string | Date): DateTime {
	const value = new Date(date);

	const formatter = new Intl.DateTimeFormat("fa-IR", {
		timeZone: "Asia/Tehran",
		year: "numeric",
		month: "2-digit",
		day: "2-digit",
		hour: "2-digit",
		minute: "2-digit",
		hour12: false,
	});

	const monthNameFormatter = new Intl.DateTimeFormat("fa-IR", {
		timeZone: "Asia/Tehran",
		month: "long",
	});

	const parts = formatter.formatToParts(value);

	const getPart = (type: Intl.DateTimeFormatPartTypes) =>
		parts.find((part) => part.type === type)?.value ?? "";

	const year = getPart("year");
	const month = getPart("month");
	const day = getPart("day");
	const hour = getPart("hour");
	const minute = getPart("minute");

	const monthName = monthNameFormatter.format(value);

	return {
		date: `${year}/${month}/${day}`,
		time: `${hour}:${minute}`,
		datetime: `${year}/${month}/${day} ${hour}:${minute}`,

		monthName,

		dateWithMonthName: `${day} ${monthName} ${year}`,

		datetimeWithMonthName: `${day} ${monthName} ${year} - ${hour}:${minute}`,

		year: Number(toEnglishDigits(year)),
		month: Number(toEnglishDigits(month)),
		day: Number(toEnglishDigits(day)),
		hour: Number(toEnglishDigits(hour)),
		minute: Number(toEnglishDigits(minute)),
	};
}
