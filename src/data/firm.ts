// firm.ts — single source of truth for the firm's shared JSON-LD entities.
// Imported into every page's @graph so the NAP/identity is defined ONCE.
// Pattern mirrors src/data/reviews.js (shared data module, not a component).

export const firmNode = {
	"@type": "LegalService",
	"@id": "https://ericblanklaw.com/#legalservice",
	name: "Eric Blank Injury Attorneys",
	image: "https://ericblanklaw.com/Eric_Blank_Injury_Attorneys_Logo.png",
	url: "https://ericblanklaw.com",
	telephone: "+1-702-222-2115",
	email: "intake@ericblanklaw.com",
	address: {
		"@type": "PostalAddress",
		streetAddress: "7860 W Sahara Ave Ste. 110",
		addressLocality: "Las Vegas",
		addressRegion: "NV",
		postalCode: "89117",
		addressCountry: "US",
	},
	geo: {
		"@type": "GeoCoordinates",
		latitude: 36.1452971,
		longitude: -115.2629678,
	},
	areaServed: [
		"Las Vegas",
		"Henderson",
		"North Las Vegas",
		"Boulder City",
		"Pahrump",
		"Clark County",
		"Nye County",
		"Nevada",
	],
	priceRange: "Contingency Fee — No Fees Unless We Win",
	openingHoursSpecification: {
		"@type": "OpeningHoursSpecification",
		dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
		opens: "00:00",
		closes: "23:59",
	},
	sameAs: [
		"https://www.facebook.com/blanklawoffices/",
		"https://www.instagram.com/ericblankinjuryattorneys/",
		"https://twitter.com/eblanklaw",
		"https://www.youtube.com/channel/UC6IixC-tkWoS1B_c8MFaHYQ",
		"https://www.tiktok.com/@ericblankinjuryattorneys",
	],
};

// TODO: ATTORNEY BIO MISSING — add  url: "https://ericblanklaw.com/attorneys/eric-r-blank"
// to attorneyNode below ONLY once that bio page actually exists and returns 200.
// Shipping a url here before the page is built = sitewide 404 in schema. Tracked in ClickUp.
export const attorneyNode = {
	"@type": "Attorney",
	"@id": "https://ericblanklaw.com/#attorney",
	name: "Eric R. Blank",
	jobTitle: "Personal Injury Attorney",
	worksFor: { "@id": "https://ericblanklaw.com/#legalservice" },
};
