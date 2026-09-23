// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://ericblanklaw.com',
  integrations: [sitemap({ filter: (page) => !page.includes('/thank-you') && !page.includes('/giveaway') })],
  vite: {
    plugins: [tailwindcss()]
  }
});
