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
        <LabArchitecture className={styles.labDiagram} role="img" aria-label="Architecture diagram of the full lab: an OPNsense firewall splitting a WAN segment holding the Kali attacker box from a LAN segment holding two domain controllers replicating with each other, an issuing CA, an AD FS server, an offline root CA, and an Ubuntu Docker host running Wazuh, Grafana, Gitea, Keycloak, a step-ca certificate authority and an nginx reverse proxy, with an OpenVAS vulnerability scanner and a Suricata sensor watching both segments, all on one computer, and the first domain controller syncing outward to a Microsoft Entra ID cloud directory." />
      </div>
    </section>
  );
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        {/* Deliberately not siteConfig.title: the navbar already renders the
            site name a few pixels above, and repeating it wastes the most
            valuable line on the page. The tagline is the most distinctive
            sentence we have, so it gets the headline. siteConfig.title still
            drives the browser tab, the metadata and the navbar. */}
        <Heading as="h1" className="hero__title">
          Build the enterprise yourself. Then defend it.
        </Heading>
        <p className="hero__subtitle">
          A free, hands-on course in infrastructure and security. Eighteen
          modules, one lab, most of it on a laptop you already own.
        </p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/course/intro">
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
