// FAQ content. Answers are plain text; blank lines start a new paragraph and lines starting with "- " become bullets.
// Based on the owner's 2020 FAQ (www.barakhadi.com/faq/), updated for the new name, price and activity count.

import { levels, site } from './site';

export interface Faq {
  q: string;
  a: string;
}

export const faqGroups: { heading: string; items: Faq[] }[] = [
  {
    heading: 'About Barakhadi',
    items: [
      {
        q: 'What is Barakhadi?',
        a: `Barakhadi is a web-based program that makes learning Marathi fun and interactive. It has ${site.activityCount} activities for conversation, reading and writing across three levels. It was created by teachers with many years of classroom experience together with technology and product experts.`,
      },
      {
        q: 'Who can use Barakhadi?',
        a: 'Anyone who wants to learn Marathi. Students use it in class and at home: in the classroom it is led by the teacher, and at home a parent can guide younger children. Teens and adults use it to learn on their own.',
      },
      {
        q: 'What are the benefits for students?',
        a: 'Activities use kid-friendly audio, video, games and drawing. Children can revisit and practice every activity as many times as they need, which strengthens their budding Marathi skills. They learn without performance pressure and explore the language on their own terms.',
      },
      {
        q: 'How is Barakhadi different from other Marathi learning apps?',
        a: 'Barakhadi is a complete, step-by-step program. Besides vocabulary and writing, it teaches through conversation, so children learn to speak Marathi and not just recognise words.',
      },
      {
        q: 'What levels are there?',
        a: `There are three levels:\n${levels.map((l) => `- ${l.name} (${l.marathi}): ${l.blurb.charAt(0).toLowerCase()}${l.blurb.slice(1, -1)}`).join('\n')}`,
      },
    ],
  },
  {
    heading: 'For Marathi shalas and teachers',
    items: [
      {
        q: 'How does it help students who already attend a BMM shala?',
        a: 'Barakhadi introduces a variety of topics for group discussion led by the teacher and lets students practice the same skills at home. Students practice conversation cues for questions, information and everyday scenarios. That builds oral fluency, vocabulary, translation, writing and comprehension skills, which are also valuable for tests.',
      },
      {
        q: "I'm a Marathi shala teacher. How is Barakhadi useful for me?",
        a: 'Lesson plans are designed week by week, so every class has a consistent structure. Each class gets its own private space: you can assign homework, grade assignments and track every student\'s progress, and students only see their own class.',
      },
      {
        q: 'Do teachers need to prepare?',
        a: 'Very little. The program is designed for 30 classes and can be used directly in the classroom. Each class has three activities: a conversation topic, a vocabulary game and writing practice. Any of them can be assigned for practice at home to extend the lesson.',
      },
      {
        q: 'Do you offer packages for schools?',
        a: 'Yes. We customise packages for Marathi shala groups based on the number of students and teachers. Contact us and tell us about your class.',
      },
    ],
  },
  {
    heading: 'Using Barakhadi',
    items: [
      {
        q: 'How does it work?',
        a: 'Barakhadi runs in the cloud. Each student gets a unique login and password and can use it from any computer or tablet with an internet connection. There is nothing to install.',
      },
      {
        q: 'Does it work on tablets and phones?',
        a: 'Yes. Barakhadi works on iPads, Android tablets, Chromebooks and computers. Phones work too, though a bigger screen makes writing activities easier.',
      },
      {
        q: 'Can my child repeat activities?',
        a: 'Yes, as many times as they like. Repetition is how language sticks.',
      },
    ],
  },
  {
    heading: 'Pricing and subscribing',
    items: [
      {
        q: 'How much does it cost?',
        a: `$${site.priceUsdPerYear} per student per level for a year (that's $5 a month). A subscription gives full access to every activity in the level you choose. For two or three levels we offer a discounted price, and school packages are customised; contact us for details.`,
      },
      {
        q: 'Can I try it before subscribing?',
        a: 'Yes. Three free activities on the home page give you a feel for the program, with no signup needed. You can also watch the three-minute intro video on the home page.',
      },
      {
        q: 'How do I subscribe?',
        a: "Contact us through the contact form or at info@barakhadi.com. We'll set up the student's account and send you the login details.",
      },
    ],
  },
];

export const allFaqs = faqGroups.flatMap((g) => g.items);
