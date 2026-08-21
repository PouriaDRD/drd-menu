import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";
import simpleImportSort from "eslint-plugin-simple-import-sort";

export default defineConfig([
	...nextVitals,
	...nextTs,

	{
		plugins: {
			"simple-import-sort": simpleImportSort,
		},

		rules: {
			"simple-import-sort/imports": [
				"error",
				{
					groups: [
						// React
						["^react$"],

						// Next
						["^next", "^next/"],

						// External packages
						["^@?\\w"],

						// Aliases (@/)
						["^@/"],

						// Side effect imports
						["^\\u0000"],

						// Parent imports
						["^\\.\\.(?!/?$)", "^\\.\\./?$"],

						// Same folder imports
						["^\\./(?=.*/)(?!/?$)", "^\\.(?!/?$)", "^\\./?$"],

						// Style imports
						["^.+\\.?(css|scss|sass)$"],
					],
				},
			],

			"simple-import-sort/exports": "error",
		},
	},

	globalIgnores([".next/**", "out/**", "build/**", "next-env.d.ts"]),
]);
