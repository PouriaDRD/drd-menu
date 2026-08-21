export function isImageFile(url: string) {
	const imageExtensions = [
		"jpg",
		"jpeg",
		"png",
		"gif",
		"webp",
		"svg",
		"avif",
		"bmp",
		"ico",
	];

	const extension = url.split(".").pop()?.split("?")[0].toLowerCase();

	return extension ? imageExtensions.includes(extension) : false;
}
