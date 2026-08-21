export function formatCardNumber(card: string) {
	// remove all non digits
	const cleaned = card.replace(/\D/g, "");

	// split every 4 digits
	return cleaned.replace(/(.{4})/g, "$1-").replace(/-$/, "");
}
