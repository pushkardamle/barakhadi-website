// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import cloudflare from '@astrojs/cloudflare';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.barakhadi.com',
  // WordPress served every page with a trailing slash (/faq/, /contact-us/). Keep it so old URLs stay valid.
  trailingSlash: 'always',
  // Optimize images at build time with sharp; no Cloudflare Images binding needed.
  adapter: cloudflare({ imageService: 'compile' }),
  devToolbar: { enabled: false },
  integrations: [sitemap({ filter: (page) => !page.includes('/thank-you') })],

  // Self-hosted from the installed Fontsource packages. Astro preloads them and generates
  // metric-matched fallbacks, so the swap to the web font doesn't shift the layout.
  fonts: [
    {
      provider: fontProviders.local(),
      name: 'Nunito',
      cssVariable: '--font-nunito',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          { src: ['@fontsource-variable/nunito/files/nunito-latin-wght-normal.woff2'], weight: '200 1000', style: 'normal' },
        ],
      },
    },
    {
      provider: fontProviders.local(),
      name: 'Outfit',
      cssVariable: '--font-outfit',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          { src: ['@fontsource/outfit/files/outfit-latin-600-normal.woff2'], weight: 600, style: 'normal' },
          { src: ['@fontsource/outfit/files/outfit-latin-700-normal.woff2'], weight: 700, style: 'normal' },
          { src: ['@fontsource/outfit/files/outfit-latin-800-normal.woff2'], weight: 800, style: 'normal' },
        ],
      },
    },
    {
      // Devanagari face for Marathi text (headline tagline, level names). Baloo 2 has proper Marathi glyphs.
      provider: fontProviders.local(),
      name: 'Baloo 2',
      cssVariable: '--font-baloo',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          { src: ['@fontsource/baloo-2/files/baloo-2-devanagari-600-normal.woff2'], weight: 600, style: 'normal' },
          { src: ['@fontsource/baloo-2/files/baloo-2-devanagari-800-normal.woff2'], weight: 800, style: 'normal' },
        ],
      },
    },
  ],

  vite: {
    plugins: [tailwindcss()],
  },
});
