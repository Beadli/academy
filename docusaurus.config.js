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

  url: 'https://academy.beadli.com',
  baseUrl: '/',

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
      announcementBar: {
        id: 'in-review-2026',
        content:
          'This course is a working draft. Every module is written but none has been walked start to finish on a clean build yet, so expect steps that skip something obvious. <strong>If you get stuck, that is the bug.</strong> <a target="_blank" rel="noopener noreferrer" href="https://github.com/Beadli/academy/issues">Tell me where it happened.</a>',
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
