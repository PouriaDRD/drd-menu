import type { MetadataRoute } from "next";

function robots(): MetadataRoute.Robots {
	return {
		rules: {
			userAgent: "*",
			allow: "/",
			disallow: ["admin", "panel", "checkout"],
		},
		sitemap: "https://menu.pouria-drd.ir/sitemap.xml",
	};
}

export default robots;
