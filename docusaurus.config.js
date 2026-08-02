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

  organizationName: 'beadli-lab-academy',
  projectName: 'academy',

  onBrokenLinks: 'throw',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          routeBasePath: 'modules',
          editUrl: 'https://github.com/beadli-lab-academy/academy/tree/main/',
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
      navbar: {
        title: 'Beadli Lab Academy',
        logo: {
          alt: 'Beadli Lab Academy',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Modules',
          },
          {
            href: 'https://github.com/beadli-lab-academy/academy',
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
            to: '/modules/intro',
          },
          {
            label: 'GitHub Discussions',
            href: 'https://github.com/beadli-lab-academy/academy/discussions',
          },
        ],
        copyright: `Course text © ${new Date().getFullYear()} Steve — CC BY-NC-SA 4.0 · Code — MIT`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['powershell', 'bash'],
      },
    }),
};

export default config;
