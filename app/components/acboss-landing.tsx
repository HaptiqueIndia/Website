"use client";

import { useState, type FormEvent, type JSX } from "react";
import {
  siteContent,
  type ComparisonRow,
  type HardwareDetail,
} from "../site-content";

type FormState = {
  name: string;
  email: string;
  city: string;
};

type FormErrors = Partial<Record<keyof FormState, string>>;

const emptyForm: FormState = {
  name: "",
  email: "",
  city: "",
};

function ComparisonTable({ rows }: { rows: readonly ComparisonRow[] }) {
  return (
    <>
      <p className="comparison-hint" id="comparison-scroll-hint">
        Scroll to compare all options.
      </p>
      <div
        aria-describedby="comparison-scroll-hint"
        aria-label="AC control comparison"
        className="comparison-table-wrap"
        role="region"
        tabIndex={0}
      >
      <table>
        <caption>How Acboss compares with common ways to control an AC</caption>
        <thead>
          <tr>
            <th scope="col">Capability</th>
            <th scope="col">Remote</th>
            <th scope="col">IR controller</th>
            <th scope="col">Smart app</th>
            <th scope="col">Acboss</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.label}>
              <th scope="row">{row.label}</th>
              <td>{row.remote}</td>
              <td>{row.irController}</td>
              <td>{row.smartApp}</td>
              <td>{row.acboss}</td>
            </tr>
          ))}
        </tbody>
      </table>
      </div>
    </>
  );
}

function HardwareDisclosure({ detail }: { detail: HardwareDetail }) {
  return (
    <details className="hardware-detail">
      <summary>{detail.name}</summary>
      <p>{detail.benefit}</p>
    </details>
  );
}

export function AcbossLanding(): JSX.Element {
  const [form, setForm] = useState<FormState>(emptyForm);
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  function updateField(field: keyof FormState, value: string) {
    setForm((current) => ({ ...current, [field]: value }));
    setErrors((current) => {
      if (!current[field]) {
        return current;
      }

      const nextErrors = { ...current };
      delete nextErrors[field];
      return nextErrors;
    });
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextErrors: FormErrors = {};

    if (!form.name.trim()) {
      nextErrors.name = "Enter your name.";
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) {
      nextErrors.email = "Enter a valid email.";
    }

    if (!form.city.trim()) {
      nextErrors.city = "Tell us your city.";
    }

    setErrors(nextErrors);

    if (Object.keys(nextErrors).length === 0) {
      setSubmitted(true);
    }
  }

  return (
    <>
      <header className="site-header">
        <nav aria-label="Primary navigation" className="site-nav">
          <a className="wordmark" href="#top" aria-label="Acboss home">
            <span aria-hidden="true">A</span>
            Acboss
          </a>
          <div className="nav-links">
            <a href="#why-acboss">Why Acboss</a>
            <a href="#how-it-works">How it works</a>
            <a href="#faq">FAQ</a>
          </div>
          <a className="nav-preorder" href="#preorder">
            Pre-order
          </a>
        </nav>
      </header>

      <main>
        <section className="hero section-shell" id="top" aria-labelledby="hero-title">
          <div className="hero-copy">
            <p className="eyebrow">Comfort that pays attention</p>
            <h1 id="hero-title">{siteContent.hero.headline}</h1>
            <p className="hero-supporting">{siteContent.hero.supporting}</p>
            <div className="hero-actions">
              <a className="button button-primary" href="#founder-story">
                See why Acboss exists
              </a>
              <a className="button button-secondary" href="#proof">
                Watch it work <span aria-hidden="true">↓</span>
              </a>
            </div>
          </div>
          <div className="hero-visual" aria-hidden="true">
            <div className="airflow airflow-one" />
            <div className="airflow airflow-two" />
            <div className="device-shadow" />
            <div className="device">
              <div className="device-face">
                <span className="device-sensor" />
                <span className="device-light" />
              </div>
              <span className="device-vent" />
            </div>
            <div className="comfort-reading">
              <span>Room comfort</span>
              <strong>Just right</strong>
            </div>
          </div>
        </section>

        <section
          className="dark-section founder-story"
          id="founder-story"
          aria-labelledby="founder-title"
        >
          <div className="section-shell story-grid">
            <p className="eyebrow eyebrow-light">{siteContent.founder.eyebrow}</p>
            <div>
              <h2 id="founder-title">
                Built after one too many uncomfortable nights.
              </h2>
              <p className="section-intro">{siteContent.founder.body}</p>
            </div>
          </div>
        </section>

        <section
          className="dark-section proof"
          id="proof"
          aria-labelledby="proof-title"
        >
          <div className="section-shell">
            <div className="section-heading">
              <p className="eyebrow eyebrow-light">Real working demos</p>
              <h2 id="proof-title">{siteContent.proof.title}</h2>
              <p>{siteContent.proof.caption}</p>
            </div>
            <div className="demo-grid">
              {siteContent.proof.demos.map((demo) => (
                <figure className="demo-card" key={demo.fallbackHref}>
                  <div className="video-frame">
                    <iframe
                      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                      allowFullScreen
                      loading="lazy"
                      referrerPolicy="strict-origin-when-cross-origin"
                      src={demo.embedSrc}
                      title={demo.title}
                    />
                  </div>
                  <figcaption>
                    <a
                      href={demo.fallbackHref}
                      rel="noreferrer"
                      target="_blank"
                    >
                      {demo.fallbackLabel}{" "}
                      <span aria-hidden="true">↗</span>
                    </a>
                  </figcaption>
                </figure>
              ))}
            </div>
          </div>
        </section>

        <section
          className="comparison section-shell"
          id="why-acboss"
          aria-labelledby="comparison-title"
        >
          <div className="section-heading">
            <p className="eyebrow">A calmer kind of control</p>
            <h2 id="comparison-title">Why Acboss is different</h2>
          </div>
          <ComparisonTable rows={siteContent.comparisonRows} />
        </section>

        <section
          className="savings section-shell"
          id="savings"
          aria-labelledby="savings-title"
        >
          <div className="savings-number" aria-hidden="true">
            <span>up to</span>
            <strong>24%</strong>
          </div>
          <div className="savings-copy">
            <p className="eyebrow">Comfort with a lighter footprint</p>
            <h2 id="savings-title">{siteContent.savings.headline}</h2>
            <div className="evidence-note">
              <p>{siteContent.savings.evidenceNote}</p>
              <p className="disclaimer">{siteContent.savings.disclaimer}</p>
            </div>
          </div>
        </section>

        <section
          className="hardware-reveal"
          id="early-build"
          aria-labelledby="hardware-title"
        >
          <div className="section-shell hardware-grid">
            <div className="hardware-intro">
              <p className="eyebrow">What early means</p>
              <h2 id="hardware-title">
                A thoughtful build, component by component
              </h2>
              <p className="section-intro">
                Each part is chosen to make your room more comfortable while
                keeping the core experience reliable and local.
              </p>
              <div className="prototype-mark">
                <span>Early build</span>
                <strong>Handmade &amp; 3D-printed</strong>
              </div>
            </div>
            <div className="hardware-list">
              {siteContent.hardwareDetails.map((detail) => (
                <HardwareDisclosure key={detail.name} detail={detail} />
              ))}
            </div>
          </div>
        </section>

        <section
          className="how-it-works section-shell"
          id="how-it-works"
          aria-labelledby="setup-title"
        >
          <div className="section-heading">
            <p className="eyebrow">Three quiet steps</p>
            <h2 id="setup-title">From setup to hands-off comfort</h2>
          </div>
          <ol className="steps">
            <li>
              <span aria-hidden="true">01</span>
              <h3>Teach it your remote</h3>
              <p>Acboss learns a compatible Split AC remote during setup.</p>
            </li>
            <li>
              <span aria-hidden="true">02</span>
              <h3>Let it read the room</h3>
              <p>Room conditions and presence inform local comfort decisions.</p>
            </li>
            <li>
              <span aria-hidden="true">03</span>
              <h3>Get comfortable</h3>
              <p>
                Acboss coordinates cooling automatically without needing the
                internet.
              </p>
            </li>
          </ol>
        </section>

        <section
          className="preorder"
          id="preorder"
          aria-labelledby="preorder-title"
        >
          <div className="section-shell preorder-grid">
            <div>
              <p className="eyebrow">Join the early access list</p>
              <h2 id="preorder-title">Request early access</h2>
              <p className="section-intro">
                {siteContent.preorder.earlyUnitNotice}
              </p>
            </div>
            {submitted ? (
              <div className="success-card" role="status" aria-live="polite">
                <span aria-hidden="true">✓</span>
                <h3>We received your early-access interest.</h3>
                <p>
                  Thank you. This records your interest only; no payment was
                  taken.
                </p>
              </div>
            ) : (
              <form className="interest-form" noValidate onSubmit={handleSubmit}>
                <div>
                  <label htmlFor="name">Name</label>
                  <input
                    id="name"
                    name="name"
                    required
                    value={form.name}
                    onChange={(event) => updateField("name", event.target.value)}
                    aria-describedby={errors.name ? "name-error" : undefined}
                    aria-invalid={Boolean(errors.name)}
                  />
                  <p className="field-error" id="name-error" aria-live="polite">
                    {errors.name}
                  </p>
                </div>

                <div>
                  <label htmlFor="email">Email</label>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    required
                    value={form.email}
                    onChange={(event) => updateField("email", event.target.value)}
                    aria-describedby={errors.email ? "email-error" : undefined}
                    aria-invalid={Boolean(errors.email)}
                  />
                  <p className="field-error" id="email-error" aria-live="polite">
                    {errors.email}
                  </p>
                </div>

                <div>
                  <label htmlFor="city">City</label>
                  <input
                    id="city"
                    name="city"
                    required
                    value={form.city}
                    onChange={(event) => updateField("city", event.target.value)}
                    aria-describedby={errors.city ? "city-error" : undefined}
                    aria-invalid={Boolean(errors.city)}
                  />
                  <p className="field-error" id="city-error" aria-live="polite">
                    {errors.city}
                  </p>
                </div>

                <button type="submit">Request early access</button>
              </form>
            )}
          </div>
        </section>

        <section
          className="faq section-shell"
          id="faq"
          aria-labelledby="faq-title"
        >
          <div className="section-heading">
            <p className="eyebrow">The practical details</p>
            <h2 id="faq-title">Frequently asked questions</h2>
          </div>
          <div className="faq-list">
            {siteContent.faqs.map((faq) => (
              <details key={faq.question}>
                <summary>{faq.question}</summary>
                <p>{faq.answer}</p>
              </details>
            ))}
          </div>
        </section>
      </main>
    </>
  );
}
