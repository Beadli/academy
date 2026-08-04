// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Beadli Lab Academy',
  tagline: 'Build the enterprise yourself. Then defend it.',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // Two deployment targets, one switch. Review phase serves from
  // beadli.github.io/academy/ (a project site, hence the path in baseUrl);
  // launch serves from academy.beadli.com at the root. Set CUSTOM_DOMAIN=1
  // in the deploy workflow to flip, rather than hand-editing three values
  // and hoping to remember all of them.
  url: process.env.CUSTOM_DOMAIN === '1'
    ? 'https://academy.beadli.com'
    : 'https://beadli.github.io',
  baseUrl: process.env.CUSTOM_DOMAIN === '1' ? '/' : '/academy/',

  organizationName: 'Beadli',
  projectName: 'academy',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  // Second docs instance for the CyberRack section. Separate from the course
  // deliberately: the curriculum runs on a laptop and buys no hardware, so
  // this content must never sit inside the module sidebar where it could be
  // mistaken for a prerequisite.
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'cyberrack',
        path: 'cyberrack',
        routeBasePath: 'cyberrack',
        sidebarPath: './sidebarsCyberrack.js',
        editUrl: 'https://github.com/Beadli/academy/tree/main/',
      },
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'course',
          editUrl: 'https://github.com/Beadli/academy/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        respectPrefersColorScheme: true,
      },
      // Review-phase notice. Remove this block at launch, once the
      // walkthrough has verified the modules on real hardware.
      //
      // One line only. The bar is a fixed-height strip above 997px, so a
      // paragraph wraps into itself. This is the whole review notice now;
      // the landing-page callout that carried the longer version was
      // removed 2026-08-03.
      //
      // Warm red rather than the brand green: the bar has to earn a click
      // from someone who came to read a course, and green reads as chrome.
      // #c0362b is the red already in the palette (lesson 0.2 role names)
      // and gives 5.5:1 against white, so it clears WCAG AA for body text.
      announcementBar: {
        id: 'in-review-2026',
        content:
          'Working draft, still being reviewed. <a target="_blank" rel="noopener noreferrer" href="https://github.com/Beadli/academy/issues">Tell me where you got stuck.</a>',
        backgroundColor: '#c0362b',
        textColor: '#ffffff',
        isCloseable: true,
      },
      navbar: {
        title: 'Beadli Lab Academy',
        logo: {
          alt: 'Beadli Lab Academy',
          // Two files rather than one currentColor file on purpose: the
          // navbar renders the logo via <img src>, which isolates the SVG
          // document, so currentColor never resolves against the page and
          // would render black in both themes.
          src: 'img/logo.svg',
          srcDark: 'img/logo-dark.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Course',
          },
          {
            type: 'docSidebar',
            docsPluginId: 'cyberrack',
            sidebarId: 'cyberrackSidebar',
            position: 'left',
            label: 'CyberRack',
          },
          {
            href: 'https://github.com/Beadli/academy',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        // Flat array (no title/items) selects Docusaurus's "simple" footer:
        // one centred row of links. Two links never justified two titled
        // columns, and the headings were most of the footer's height.
        links: [
          {
            label: 'Start with Module 0',
            to: '/course/intro',
          },
          {
            label: 'About',
            to: '/about',
          },
          {
            label: 'GitHub Discussions',
            href: 'https://github.com/Beadli/academy/discussions',
          },
        ],
        // Names the brand rather than a person deliberately: LICENSE-CONTENT.md
        // requires attribution to "Beadli Lab Academy", and for a CC BY licence
        // the notice's job is to name the party reusers must credit. A personal
        // name here would contradict it.
        copyright: `Course text © ${new Date().getFullYear()} Beadli Lab Academy · CC BY-NC-SA 4.0 · Code MIT`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['powershell', 'bash'],
      },
    }),
};

export default config;
