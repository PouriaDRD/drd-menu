import type { MetadataRoute } from "next";

function siteMap(): MetadataRoute.Sitemap {
	return [
		{
			url: "https://menu.pouria-drd.ir",
			lastModified: "07/22/2026",
			changeFrequency: "monthly",
			priority: 1,
		},
	];
}
export default siteMap;
