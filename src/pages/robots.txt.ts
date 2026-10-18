// robots.txt follows site.launched: crawlers are blocked until the site goes live on www.barakhadi.com.
import type { APIRoute } from 'astro';
import { site } from '@/data/site';

export const GET: APIRoute = () => {
  const body = site.launched
    ? `User-agent: *\nAllow: /\n\nSitemap: ${new URL('/sitemap-index.xml', site.url).href}\n`
    : 'User-agent: *\nDisallow: /\n';
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
