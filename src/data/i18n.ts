// i18n.ts — single source of truth for the EN ↔ ES URL pairs.
// Keys are English paths, values are their Spanish counterparts.
// Both sides use the trailing-slash (canonical) form.
//
// Used by:
//   - BaseHead.astro  → emits hreflang alternate links automatically on BOTH
//     languages' pages (bidirectional, as Google requires). A page whose path
//     is not in this map simply gets no hreflang tags (e.g. /blog/ for now).
//   - Header.astro    → the ES/EN language toggle links to the counterpart page.
//
// RULE: every new Spanish page gets a row here, and every row must have both
// files existing — BaseHead will happily emit a hreflang pointing at a 404
// if a row is added before the page is built.

export const esRoutes: Record<string, string> = {
	"/": "/es/",
	"/about/": "/es/sobre-nosotros/",
	"/attorneys/": "/es/abogados/",
	"/attorneys/eric-blank/": "/es/abogados/eric-blank/",
	"/attorneys/fikisha-miller/": "/es/abogados/fikisha-miller/",
	"/practice-areas/": "/es/areas-de-practica/",
	"/practice-areas/car-accidents/": "/es/areas-de-practica/accidentes-de-auto/",
	"/practice-areas/motorcycle-accidents/": "/es/areas-de-practica/accidentes-de-motocicleta/",
	"/practice-areas/truck-accidents/": "/es/areas-de-practica/accidentes-de-camion/",
	"/practice-areas/rideshare-accidents/": "/es/areas-de-practica/accidentes-de-uber-y-lyft/",
	"/practice-areas/slip-and-fall/": "/es/areas-de-practica/resbalones-y-caidas/",
	"/practice-areas/dog-bites/": "/es/areas-de-practica/mordeduras-de-perro/",
	"/practice-areas/workers-compensation/": "/es/areas-de-practica/compensacion-laboral/",
	"/practice-areas/brain-and-spine-injury/": "/es/areas-de-practica/lesiones-cerebrales-y-de-columna/",
	"/practice-areas/pedestrian-accidents/": "/es/areas-de-practica/atropellos-de-peatones/",
	"/practice-areas/bicycle-accidents/": "/es/areas-de-practica/accidentes-de-bicicleta/",
	"/practice-areas/wrongful-death/": "/es/areas-de-practica/muerte-injusta/",
	"/practice-areas/casino-injuries/": "/es/areas-de-practica/lesiones-en-casinos/",
	"/practice-areas/boating-accidents/": "/es/areas-de-practica/accidentes-de-embarcaciones/",
	"/practice-areas/bus-accidents/": "/es/areas-de-practica/accidentes-de-autobus/",
	"/practice-areas/dui-accidents/": "/es/areas-de-practica/accidentes-por-conductor-ebrio/",
	"/practice-areas/criminal-law/": "/es/areas-de-practica/derecho-penal/",
	"/practice-areas/mass-tort/": "/es/areas-de-practica/litigios-masivos/",
	"/practice-areas/products-liability/": "/es/areas-de-practica/productos-defectuosos/",
	"/practice-areas/school-bullying/": "/es/areas-de-practica/acoso-escolar/",
	"/practice-areas/sexual-assault/": "/es/areas-de-practica/agresion-sexual/",
	"/contact/": "/es/contacto/",
	"/results/": "/es/resultados/",
	"/reviews/": "/es/resenas/",
	"/faq/": "/es/preguntas-frecuentes/",
	"/careers/": "/es/empleo/",
	"/privacy-policy/": "/es/politica-de-privacidad/",
	"/terms-of-use/": "/es/terminos-de-uso/",
	"/thank-you/": "/es/gracias/",
	"/lp/las-vegas-accident-attorney/": "/es/lp/abogado-de-accidentes-las-vegas/",
	"/lp/las-vegas-car-accident-attorney/": "/es/lp/abogado-de-accidentes-de-auto-las-vegas/",
	"/lp/las-vegas-motorcycle-injury-attorney/": "/es/lp/abogado-de-accidentes-de-motocicleta-las-vegas/",
	"/lp/las-vegas-rideshare-injury-attorney/": "/es/lp/abogado-de-accidentes-de-uber-y-lyft-las-vegas/",
	"/lp/clark-county-personal-injury-attorney/": "/es/lp/abogado-de-lesiones-personales-condado-de-clark/",
	"/lp/clark-county-boating-injury-attorney/": "/es/lp/abogado-de-accidentes-de-embarcaciones-condado-de-clark/",
	"/lp/clark-county-casino-injury-attorney/": "/es/lp/abogado-de-lesiones-en-casinos-condado-de-clark/",
	"/lp/clark-county-slip-and-fall-attorney/": "/es/lp/abogado-de-resbalones-y-caidas-condado-de-clark/",
	"/lp/clark-county-truck-accident-attorney/": "/es/lp/abogado-de-accidentes-de-camion-condado-de-clark/",
	"/lp/school-bullying-lawsuit-attorney/": "/es/lp/abogado-de-acoso-escolar/",
};

// Reverse map: Spanish path → English path.
export const enRoutes: Record<string, string> = Object.fromEntries(
	Object.entries(esRoutes).map(([en, es]) => [es, en]),
);

/** Normalize a pathname to its trailing-slash form ("/about" → "/about/"). */
function normalize(pathname: string): string {
	if (pathname.endsWith("/")) return pathname;
	const last = pathname.split("/").pop() ?? "";
	return last.includes(".") ? pathname : pathname + "/";
}

/**
 * Given the current pathname (either language), return its { en, es } pair,
 * or null when the page has no counterpart (e.g. blog pages for now).
 */
export function altFor(pathname: string): { en: string; es: string } | null {
	const p = normalize(pathname);
	if (p in esRoutes) return { en: p, es: esRoutes[p] };
	if (p in enRoutes) return { en: enRoutes[p], es: p };
	return null;
}
