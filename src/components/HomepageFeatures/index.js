import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'One lab, built by you',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Not isolated exercises. Every module adds to the same environment —
        Active Directory, PKI, SSO, Docker, Ansible, monitoring — until you
        are running a mock enterprise on your own hardware.
      </>
    ),
  },
  {
    title: 'The why, not just the how',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Every step explains the concept behind it and how it plays out in a
        real enterprise, with war stories from a lab that actually runs.
        A 16 GB laptop gets you through most of it.
      </>
    ),
  },
  {
    title: 'Then attack it',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Kali against your own lab: run the attacks, watch your detections
        fire, tune them, repeat. Finish with an incident investigation in
        infrastructure you built from nothing.
      </>
    ),
  },
  {
    title: 'AI as a working tool',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        You&apos;ll work with Claude from Module 1 the way engineers actually
        do — troubleshooting errors, drafting docs from your shell history,
        reviewing configs — and learn the discipline that goes with it:
        verify before you run, never paste secrets, understand before you
        apply.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--6')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
