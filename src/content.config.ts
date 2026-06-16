import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
	// Astro v6 glob loader — plain Markdown posts under src/content/blog
	loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
	schema: z.object({
		title: z.string(),
		description: z.string(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		author: z.string().default('Eric Blank Injury Attorneys'),
		heroImage: z.string().optional(),
		draft: z.boolean().default(false),
	}),
});

export const collections = { blog };
