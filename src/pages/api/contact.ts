// Contact form endpoint: verifies Cloudflare Turnstile, then emails the message to info@ through Resend.
// Secrets (set with `npx wrangler secret put NAME`, locally in .dev.vars):
//   TURNSTILE_SECRET_KEY  Turnstile secret for the site key used on /contact-us/
//   RESEND_API_KEY        Resend API key (barakhadi.com verified as a sending domain)
// Optional vars: CONTACT_TO (default info@barakhadi.com), CONTACT_FROM (default website@barakhadi.com).
import type { APIRoute } from 'astro';
import { env } from 'cloudflare:workers';
import { site } from '@/data/site';

export const prerender = false;

const TOPICS: Record<string, string> = {
  subscribe: 'Subscribing a student',
  levels: 'Multi-level pricing',
  school: 'Marathi shala package',
  support: 'Account help',
  other: 'Other',
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

export const POST: APIRoute = async ({ request, clientAddress }) => {
  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return json({ ok: false, error: 'The form could not be read. Please try again.' }, 400);
  }

  const field = (name: string, max: number) => String(form.get(name) ?? '').trim().slice(0, max);
  const name = field('name', 100);
  const email = field('email', 200);
  const message = field('message', 5000);
  const phone = field('phone', 30);
  const location = field('location', 100);
  const topic = TOPICS[field('topic', 20)];

  // Honeypot filled in: pretend it worked so bots don't retry.
  if (field('company', 200)) return json({ ok: true });

  if (!name || !email || !message) {
    return json({ ok: false, error: 'Please fill in your name, email and message.' }, 400);
  }
  if (!topic) {
    return json({ ok: false, error: 'Please choose what your message is about.' }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ ok: false, error: "That email address doesn't look right. Please check it." }, 400);
  }

  const vars = env as unknown as Record<string, string | undefined>;

  // Turnstile check
  const token = field('cf-turnstile-response', 2048);
  const secret = vars.TURNSTILE_SECRET_KEY ?? (import.meta.env.DEV ? '1x0000000000000000000000000000000AA' : undefined);
  if (!secret) {
    console.error('contact: TURNSTILE_SECRET_KEY is not set');
    return json({ ok: false, error: `The form isn't working right now. Please email us at ${site.email}.` }, 500);
  }
  const verify = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({ secret, response: token, remoteip: clientAddress ?? '' }),
  });
  const outcome = (await verify.json().catch(() => ({}))) as { success?: boolean };
  if (!outcome.success) {
    return json({ ok: false, error: 'Please complete the "verify you are human" check and send again.' }, 400);
  }

  const text = [
    'New message from the Barakhadi website',
    '',
    `Name: ${name}`,
    `Email: ${email}`,
    `Phone: ${phone || '(not given)'}`,
    `City, country: ${location || '(not given)'}`,
    `Topic: ${topic}`,
    '',
    message,
    '',
  ].join('\n');

  if (!vars.RESEND_API_KEY) {
    if (import.meta.env.DEV) {
      console.log('contact (dev, not sent):\n' + text);
      return json({ ok: true });
    }
    console.error('contact: RESEND_API_KEY is not set');
    return json({ ok: false, error: `The form isn't working right now. Please email us at ${site.email}.` }, 500);
  }

  const send = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${vars.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: `Barakhadi website <${vars.CONTACT_FROM ?? 'website@barakhadi.com'}>`,
      to: [vars.CONTACT_TO ?? site.email],
      reply_to: email,
      subject: `Website: ${topic} (${name})`,
      text,
    }),
  });

  if (!send.ok) {
    console.error('contact: Resend error', send.status, await send.text());
    return json({ ok: false, error: `Your message could not be sent. Please email us at ${site.email}.` }, 502);
  }
  return json({ ok: true });
};
