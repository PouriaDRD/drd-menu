import { PropsWithChildren } from "react";

import type { Metadata } from "next";
import { Geist, Geist_Mono, Inter } from "next/font/google";
import localFont from "next/font/local";

import { UserProvider } from "@/features/accounts/context";
import { QCProvider } from "@/features/api/contexts";
import { ThemeProvider } from "@/features/preferences/contexts";
import { AppToaster } from "@/features/shared/contexts";
import { cn } from "@/features/shared/utils";

import "./globals.css";

const SITE_NAME = "DRD Menu";
const SITE_TITLE = "DRD Menu";
const SITE_DESCRIPTION = "DRD Menu";

const SITE_URL = "https://menu.pouria-drd.ir";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
	metadataBase: new URL(SITE_URL),

	manifest: "/manifest.webmanifest",

	title: {
		default: SITE_NAME,
		template: "DRD Menu | %s",
	},

	description: SITE_DESCRIPTION,

	applicationName: SITE_NAME,

	referrer: "origin-when-cross-origin",

	category: "technology",

	creator: "Pouria Darandi",

	publisher: SITE_NAME,

	authors: [
		{
			name: "Pouria Darandi",
			url: "https://pouria-drd.ir",
		},
	],

	alternates: {
		canonical: "/",
	},

	appleWebApp: {
		title: SITE_NAME,
		statusBarStyle: "default",
		capable: true,
	},

	openGraph: {
		type: "website",

		locale: "fa_IR",

		url: "/",

		siteName: SITE_NAME,

		title: SITE_TITLE,

		description: SITE_DESCRIPTION,

		images: [
			{
				url: "/opengraph-image.png",
				width: 1200,
				height: 630,
				alt: SITE_NAME,
			},
		],
	},

	twitter: {
		card: "summary_large_image",

		site: "@pouria_drd",

		creator: "@pouria_drd",

		title: SITE_TITLE,

		description: SITE_DESCRIPTION,

		images: ["/twitter-image.png"],
	},

	robots: {
		index: true,

		follow: true,

		nocache: false,

		googleBot: {
			index: true,

			follow: true,

			"max-image-preview": "large",
		},
	},

	verification: {
		// Search Console value for "Google Search Console/Site Verification"
		google: "",
	},
};

export default function RootLayout({ children }: Readonly<PropsWithChildren>) {
	return (
		<html
			dir="rtl"
			lang="fa-IR"
			suppressHydrationWarning
			data-scroll-behavior="smooth"
			className={cn(
				"h-full",
				"antialiased",
				geistSans.variable,
				geistMono.variable,
				"font-sans",
				inter.variable,
				peyda.variable,
				iranYekanX.variable,
				"ss02",
			)}>
			<body
				suppressHydrationWarning
				className="min-h-full flex flex-col font-iran-yekan-x! ss02 h-full">
				<QCProvider>
					<ThemeProvider
						attribute="class"
						defaultTheme="system"
						enableSystem
						disableTransitionOnChange>
						<AppToaster />
						<UserProvider>
							<div className="h-full flex-1">{children}</div>
						</UserProvider>
					</ThemeProvider>
				</QCProvider>
			</body>
		</html>
	);
}

const geistSans = Geist({
	variable: "--font-geist-sans",
	subsets: ["latin"],
});

const geistMono = Geist_Mono({
	variable: "--font-geist-mono",
	subsets: ["latin"],
});

const peyda = localFont({
	src: [
		{
			weight: "100",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Thin.woff2",
		},
		{
			weight: "200",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-ExtraLight.woff2",
		},
		{
			weight: "300",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Light.woff2",
		},
		{
			weight: "400",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Regular.woff2",
		},
		{
			weight: "500",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Medium.woff2",
		},
		{
			weight: "600",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-SemiBold.woff2",
		},
		{
			weight: "700",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Bold.woff2",
		},
		{
			weight: "800",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-ExtraBold.woff2",
		},
		{
			weight: "900",
			style: "normal",
			path: "./assets/fonts/Peyda/woff2/PeydaWebFaNum-Black.woff2",
		},
	],
	variable: "--font-peyda",
});

const iranYekanX = localFont({
	src: [
		{
			weight: "normal",
			style: "normal",
			path: "./assets/fonts/IRANYekanX/IRANYekanX-Regular.woff",
		},
		{
			weight: "bold",
			style: "normal",
			path: "./assets/fonts/IRANYekanX/IRANYekanX-Bold.woff",
		},
	],
	variable: "--font-iran-yekan-x",
});
