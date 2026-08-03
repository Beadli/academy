import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'One lab, built by you',
    Svg: require('@site/static/img/card-lab.svg').default,
    description: (
      <>
        Every module adds to the same environment: Active Directory, PKI,
        single sign-on, Docker, Ansible, monitoring. By the capstone you are
        running a mock enterprise on your own hardware, not a pile of
        disconnected exercises, and you&apos;ll have assessed it for
        compliance the way an auditor would.
      </>
    ),
  },
  {
    title: 'You will know why it works',
    Svg: require('@site/static/img/card-why.svg').default,
    description: (
      <>
        Every step explains the concept behind it and how the same thing is
        done in a real enterprise. The war stories come from a lab that
        exists and breaks like any other. A 16 GB laptop gets you through
        most of it.
      </>
    ),
  },
  {
    title: 'Then attack it',
    Svg: require('@site/static/img/card-attack.svg').default,
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
    Svg: require('@site/static/img/card-ai.svg').default,
    description: (
      <>
        Claude is part of the toolkit from Module 1, used the way working
        engineers use it: troubleshooting errors, turning shell history into
        documentation, reviewing configs before they ship. With two rules
        that matter more than any prompt: understand a command before you
        run it, and keep secrets out of the chat window.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--6', styles.featureCard)}>
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
