import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
	return {
		name: "DRD Shop",
		short_name: "DRD Shop",
		description:
			"دی‌آردی شاپ ارائه‌دهنده سرویس‌های VPN پرسرعت، پایدار و اقتصادی با پشتیبانی حرفه‌ای و فعال برای کاربران ایران.",
		start_url: "/panel/dashboard",
		display: "standalone",
		background_color: "#f9f9f9",
		theme_color: "#1447e6",
		icons: [
			{
				src: "/images/web-app-manifest-192x192.png",
				sizes: "192x192",
				type: "image/png",
			},
			{
				src: "/images/web-app-manifest-512x512.png",
				sizes: "512x512",
				type: "image/png",
			},
		],
	};
}
