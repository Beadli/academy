import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import Heading from '@theme/Heading';
import styles from './index.module.css';
import LabArchitecture from '@site/static/img/lab-architecture.svg';

function LabPreview() {
  return (
    <section className={styles.labSection}>
      <div className="container">
        <Heading as="h2">The lab you'll build</Heading>
        <p className={styles.labCaption}>
          Every module adds a piece. This is where you end up: a segmented,
          monitored, attacked-and-defended enterprise, on one machine, which
          you then sync to a cloud tenant the way real hybrid environments
          do. The tier badges show when each piece arrives.
        </p>
        <LabArchitecture className={styles.labDiagram} role="img" aria-label="Architecture diagram of the full lab: an OPNsense firewall splitting a WAN segment holding the Kali attacker box from a LAN segment holding the domain controller, issuing CA, AD FS server, offline root CA, and an Ubuntu Docker host running Wazuh, Grafana and Gitea, with a Suricata sensor watching both segments, all on one laptop, and the domain controller syncing outward to a Microsoft Entra ID cloud directory." />
      </div>
    </section>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/modules/intro">
            Start with Module 0
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={siteConfig.title}
      description="A free, hands-on infrastructure and security curriculum: build, operate, defend, and attack your own mock enterprise.">
      <HomepageHeader />
      <main>
        <LabPreview />
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
