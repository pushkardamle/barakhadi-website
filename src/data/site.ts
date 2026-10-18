// Site-wide facts and links. Change them here, not in components.

export const site = {
  // false while the site lives on a staging URL: every page gets noindex and robots.txt blocks crawlers.
  // Flip to true at launch on www.barakhadi.com.
  launched: false,
  name: 'Barakhadi',
  nameMarathi: 'बाराखडी',
  company: 'Barakhadi LLC',
  url: 'https://www.barakhadi.com',
  email: 'info@barakhadi.com',
  tagline: 'Learn Marathi the Fun Way',
  taglineMarathi: 'चला शिकू या मराठी',
  description:
    'Learn Marathi the fun way. 300+ interactive activities for kids to read, write and speak Marathi, made by experienced Marathi teachers.',
  // Per student, per level, per year. More than one level: discounted price on request.
  priceUsdPerYear: 60,
  activityCount: '300+',
  conversationTopics: 30,
};

// TalentLMS. Schools log in at the main portal; self-learners will use the indml branch (Phase 2).
export const lms = {
  loginUrl: 'https://marathi.talentlms.com',
  selfLearnerLoginUrl: 'https://indml-marathi.talentlms.com',
};

// Free guest activities on TalentLMS (no signup). One per sample on the home page.
export const freeActivities = [
  {
    key: 'conversation',
    title: 'Conversation',
    subtitle: 'Family introductions',
    description: 'Introduce yourself and your family members in Marathi.',
    glyph: 'गप्पा',
    url: 'https://marathi.talentlms.com/shared/start/key:EOSNHRKM',
  },
  {
    key: 'vocabulary',
    title: 'Vocabulary',
    subtitle: 'Words with ड',
    description: 'Learn words that start with the letter ड, with pictures and clear audio.',
    glyph: 'ड',
    url: 'https://marathi.talentlms.com/shared/start/key:EQLNHRKM',
  },
  {
    key: 'writing',
    title: 'Writing',
    subtitle: 'Trace the letter ग',
    description: 'Trace and write ग step by step, as many times as you like.',
    glyph: 'ग',
    url: 'https://marathi.talentlms.com/shared/start/key:EGBNHRKM',
  },
] as const;

export const levels = [
  { id: 0, name: 'Level 0', marathi: 'शिशु वर्ग', blurb: 'First letters, sounds and everyday words.' },
  { id: 1, name: 'Level 1', marathi: 'पहिली', blurb: 'Reading and writing letters and simple words.' },
  { id: 2, name: 'Level 2', marathi: 'दुसरी', blurb: 'Matras, longer words and short sentences.' },
] as const;

// Wistia media ID of the public intro video. (The full demo and teacher-training videos were made
// for one Marathi school and must not appear on the public site.)
export const videos = {
  homeDemo: 'ktanuvwk0f',
};

export const nav = [
  { href: '/who-its-for/', label: "Who it's for" },
  { href: '/pricing/', label: 'Pricing' },
  { href: '/about/', label: 'About' },
  { href: '/faq/', label: 'FAQ' },
  { href: '/contact-us/', label: 'Contact' },
];

export const footerNav = [
  {
    heading: 'Barakhadi',
    links: [
      { href: '/who-its-for/', label: "Who it's for" },
      { href: '/pricing/', label: 'Pricing' },
      { href: '/#try-free', label: 'Free activities' },
    ],
  },
  {
    heading: 'Company',
    links: [
      { href: '/about/', label: 'About us' },
      { href: '/faq/', label: 'FAQ' },
      { href: '/contact-us/', label: 'Contact' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { href: '/privacy/', label: 'Privacy policy' },
      { href: '/terms/', label: 'Terms of service' },
    ],
  },
];
