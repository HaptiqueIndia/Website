# Acboss Customer Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a responsive Acboss customer website that earns a pre-order through a founder-led comfort story, real working-product proof, and a clear edge-AI comparison.

**Architecture:** A single Vinext/React route renders one composed landing-page component fed by a typed local content module. Local components own navigation, accessible FAQ disclosure, and client-only pre-order validation; all marketing copy, comparison data, and evidence metadata remain in the content module so real prototype assets can be changed without restructuring the page.

**Tech Stack:** Vinext, React, TypeScript, CSS, Vitest, Testing Library, Sites hosting.

## Global Constraints

- Initialize the empty workspace with the Sites starter and preserve its package manager, scripts, Vite plugin, and `.openai/hosting.json`.
- Publish one customer-focused route only; do not add accounts, payments, a database, or checkout.
- Hero headline: “Your AC, finally on autopilot.” Supporting line: “More comfort. Less energy. Zero manual fiddling.”
- The hero must lead to the founder story and working demo, not pre-order. Pre-order belongs in navigation and the final conversion section.
- Savings claims must not exceed “up to 24%”; all savings evidence must say results vary by home and use.
- Present the founder’s experience as a personal comfort story, never as medical treatment, prevention, or diagnosis.
- Describe Matter as “Matter-ready,” never Matter-certified before certification is earned.
- Clearly describe the launch product as a handmade early unit with a 3D-printed enclosure; do not imply mass-production readiness or unverified compatibility.
- Before asset integration, obtain a real Split AC demo video and a redacted electricity-bill image. Never use fabricated proof media or expose a bill number, address, or account holder.
- Respect `prefers-reduced-motion`, keyboard navigation, visible focus, and mobile layouts without horizontal overflow.

---

## File Structure

| File | Responsibility |
| --- | --- |
| `.openai/hosting.json` | Retained Sites deployment configuration produced by the starter. |
| `package.json` | Retained project scripts plus explicit `test` script. |
| `app/layout.tsx` | Site metadata, global font imports, and Open Graph/X metadata. |
| `app/layout.test.ts` | Tests for product-specific title and description metadata. |
| `app/page.tsx` | Server route that renders the Acboss landing page. |
| `app/site-content.ts` | Typed marketing copy, comparisons, FAQs, proof metadata, hardware details, and guardrail strings. |
| `app/site-content.test.ts` | Tests protecting claim caps, required disclaimers, and technical wording. |
| `app/components/acboss-landing.tsx` | Client component for the page sections, responsive navigation, FAQ, anchors, and validated pre-order form. |
| `app/components/acboss-landing.test.tsx` | Interaction tests for anchors, FAQ, and pre-order validation/confirmation. |
| `app/globals.css` | Full responsive visual system, product visual, page composition, and reduced-motion rules. |
| `public/proof/split-ac-demo.mp4` | User-supplied, captioned working-product demo; required before publishing. |
| `public/proof/split-ac-demo-poster.webp` | Poster still from the real demo; required before publishing. |
| `public/proof/bill-savings-redacted.webp` | User-supplied and redacted electricity-bill evidence; required before publishing. |
| `public/og.png` | Site-specific social preview generated only after the final design and copy are stable. |

### Task 1: Initialize the one-page site and test harness

**Files:**
- Create: starter-produced `package.json`, `app/page.tsx`, `app/layout.tsx`, `app/globals.css`, `.openai/hosting.json`
- Modify: `package.json`
- Create: `vitest.config.ts`, `app/test/setup.ts`

**Interfaces:**
- Produces: a healthy Vinext app with `npm run dev`, `npm run build`, and `npm run test` commands.
- Produces: `app/test/setup.ts` importing `@testing-library/jest-dom/vitest` for component assertions.

- [ ] **Step 1: Initialize the site exactly once**

Run:

```bash
bash /Users/willisdesai/.codex/plugins/cache/openai-bundled/sites/0.1.31/scripts/init-site.sh "$PWD"
```

Expected: starter files exist, `.openai/hosting.json` exists, and the chosen package manager lockfile is created.

- [ ] **Step 2: Start the development server and open its one local preview**

Run:

```bash
npm run dev
```

Expected: one healthy local URL; keep this process alive for HMR while building.

- [ ] **Step 3: Add the failing test command and test environment**

Install only the development dependencies required for TypeScript component tests, then add this exact script to `package.json`:

```json
{
  "scripts": {
    "test": "vitest run"
  }
}
```

Create `vitest.config.ts`:

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: { environment: "jsdom", setupFiles: ["./app/test/setup.ts"] },
});
```

Create `app/test/setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";
```

- [ ] **Step 4: Run the empty test command to verify the harness**

Run:

```bash
npm run test
```

Expected: exits successfully with no tests yet discovered.

- [ ] **Step 5: Commit the initialized site when Git is available**

Run:

```bash
git add .openai package.json app vitest.config.ts
git commit -m "chore: initialize Acboss customer site"
```

Expected: one commit containing only the starter and test harness. If the workspace has not been initialized as a Git repository, skip this command and record that fact in the execution handoff.

### Task 2: Define the evidence-safe marketing content

**Files:**
- Create: `app/site-content.ts`
- Create: `app/site-content.test.ts`

**Interfaces:**
- Produces: `siteContent` with `hero`, `comparisonRows`, `hardwareDetails`, `faqs`, `proof`, and `preorder` properties.
- Produces: `ComparisonRow = { label: string; remote: string; irController: string; smartApp: string; acboss: string }`.
- Produces: `HardwareDetail = { name: string; benefit: string }`.

- [ ] **Step 1: Write the failing content-guardrail tests**

Create `app/site-content.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { siteContent } from "./site-content";

describe("Acboss customer claims", () => {
  it("caps the headline savings claim at 24% and retains the variance disclaimer", () => {
    expect(siteContent.savings.headline).toContain("up to 24%");
    expect(siteContent.savings.disclaimer).toMatch(/results vary/i);
  });

  it("keeps Matter language future-facing and avoids certification claims", () => {
    const matter = siteContent.hardwareDetails.find((item) => item.name === "Matter-ready platform");
    expect(matter?.benefit).toMatch(/future Matter path/i);
    expect(matter?.benefit).not.toMatch(/Matter-certified/i);
  });

  it("makes the early-unit nature explicit", () => {
    expect(siteContent.preorder.earlyUnitNotice).toMatch(/handmade/i);
    expect(siteContent.preorder.earlyUnitNotice).toMatch(/3D-printed/i);
  });
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
npm run test -- app/site-content.test.ts
```

Expected: FAIL because `./site-content` does not exist.

- [ ] **Step 3: Implement the typed content module**

Create `app/site-content.ts` using this interface and required values:

```ts
export type ComparisonRow = {
  label: string;
  remote: string;
  irController: string;
  smartApp: string;
  acboss: string;
};

export type HardwareDetail = { name: string; benefit: string };

export const siteContent = {
  hero: {
    headline: "Your AC, finally on autopilot.",
    supporting: "More comfort. Less energy. Zero manual fiddling.",
  },
  founder: {
    eyebrow: "Cold is not always comfortable.",
    body: "Acboss began with a familiar problem: waking up in an over-cooled, dry room and another uncomfortable morning. We built a better way to cool—one that responds to the room instead of making you keep reaching for the remote.",
  },
  proof: {
    videoSrc: "/proof/split-ac-demo.mp4",
    posterSrc: "/proof/split-ac-demo-poster.webp",
    title: "Acboss working with a Split AC",
    caption: "Tested and iterated as working prototypes over five months.",
  },
  savings: {
    headline: "Designed to use up to 24% less energy for cooling.",
    disclaimer: "Results vary by home, weather, AC, and use.",
    billImageSrc: "/proof/bill-savings-redacted.webp",
    billImageAlt: "Redacted electricity bill comparison used in Acboss testing",
  },
  comparisonRows: [
    { label: "Feels the room, not just the AC", remote: "No", irController: "No", smartApp: "No", acboss: "Yes — temperature and humidity aware" },
    { label: "Adjusts cooling by itself", remote: "No", irController: "Usually manual or scheduled", smartApp: "Usually manual or scheduled", acboss: "Yes — continuously optimizes comfort" },
    { label: "Coordinates AC and fan", remote: "No", irController: "No", smartApp: "Rarely", acboss: "Yes — optimized together" },
    { label: "Works when internet is down", remote: "Yes", irController: "Often", smartApp: "Usually no", acboss: "Yes — entirely local" },
    { label: "Learns the right cooling response", remote: "No", irController: "No", smartApp: "No", acboss: "Yes — edge logic built for Indian conditions" },
  ] satisfies ComparisonRow[],
  hardwareDetails: [
    { name: "ESP32-C5 controller", benefit: "Provides the processing foundation and supports both 5 GHz and 2.4 GHz Wi-Fi capability." },
    { name: "Human-presence sensor", benefit: "Lets Acboss understand whether a person is in the room before making comfort decisions." },
    { name: "IR transmitter and receiver", benefit: "Learns your AC remote during setup, then controls the existing Split AC." },
    { name: "Sensirion temperature and humidity sensor", benefit: "Provides accurate room-condition inputs for Acboss’s local comfort logic." },
    { name: "Matter-ready platform", benefit: "Designed for a future Matter path; it is Matter-ready, not Matter-certified." },
  ] satisfies HardwareDetail[],
  faqs: [
    { question: "Will Acboss work with my AC?", answer: "Acboss is designed to learn compatible infrared Split AC remotes during setup. Early availability is limited to tested setups." },
    { question: "Does Acboss need Wi-Fi?", answer: "No. Its comfort decisions run locally, so the core experience does not depend on an internet connection." },
    { question: "What does an early unit look like?", answer: "It is a handmade, 3D-printed build from our tested prototype platform." },
  ],
  preorder: {
    earlyUnitNotice: "Early Acboss units are handmade, 3D-printed builds from our tested prototype platform.",
  },
} as const;
```

Keep the exact customer-facing data shown above. Do not add unverified competitor claims or certification wording.

- [ ] **Step 4: Run the focused test to verify it passes**

Run:

```bash
npm run test -- app/site-content.test.ts
```

Expected: PASS with all three guardrail assertions.

- [ ] **Step 5: Commit the content boundary**

Run:

```bash
git add app/site-content.ts app/site-content.test.ts
git commit -m "feat: add evidence-safe Acboss content"
```

Expected: a focused content-and-tests commit.

### Task 3: Build the accessible customer journey and conversion behavior

**Files:**
- Create: `app/components/acboss-landing.tsx`
- Create: `app/components/acboss-landing.test.tsx`
- Modify: `app/page.tsx`

**Interfaces:**
- Consumes: `siteContent`, `ComparisonRow`, and `HardwareDetail` from `app/site-content.ts`.
- Produces: `AcbossLanding(): JSX.Element`.
- Produces: form state `{ name: string; email: string; city: string }` and an in-page confirmation state after valid submission.

- [ ] **Step 1: Write failing interaction tests**

Create `app/components/acboss-landing.test.tsx`:

```tsx
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AcbossLanding } from "./acboss-landing";

describe("AcbossLanding", () => {
  it("does not lead the hero with a pre-order action", () => {
    render(<AcbossLanding />);
    expect(screen.getByRole("link", { name: /see why acboss exists/i })).toHaveAttribute("href", "#founder-story");
    expect(screen.getByRole("link", { name: /watch it work/i })).toHaveAttribute("href", "#proof");
  });

  it("keeps invalid pre-order fields visible with specific errors", () => {
    render(<AcbossLanding />);
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));
    expect(screen.getByText(/enter your name/i)).toBeVisible();
    expect(screen.getByText(/enter a valid email/i)).toBeVisible();
    expect(screen.getByText(/tell us your city/i)).toBeVisible();
  });

  it("confirms interest without claiming payment", () => {
    render(<AcbossLanding />);
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: "Asha" } });
    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "asha@example.com" } });
    fireEvent.change(screen.getByLabelText(/city/i), { target: { value: "Pune" } });
    fireEvent.click(screen.getByRole("button", { name: /request early access/i }));
    expect(screen.getByText(/we received your early-access interest/i)).toBeVisible();
    expect(screen.queryByText(/payment received/i)).not.toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run the component test to verify it fails**

Run:

```bash
npm run test -- app/components/acboss-landing.test.tsx
```

Expected: FAIL because `./acboss-landing` does not exist.

- [ ] **Step 3: Implement `AcbossLanding` with semantic sections**

Create `app/components/acboss-landing.tsx` as a client component. It must render these exact section IDs in this narrative order:

```tsx
<main>
  <section id="top" aria-labelledby="hero-title" />
  <section id="founder-story" aria-labelledby="founder-title" />
  <section id="proof" aria-labelledby="proof-title" />
  <section id="why-acboss" aria-labelledby="comparison-title" />
  <section id="savings" aria-labelledby="savings-title" />
  <section id="early-build" aria-labelledby="hardware-title" />
  <section id="how-it-works" aria-labelledby="setup-title" />
  <section id="preorder" aria-labelledby="preorder-title" />
  <section id="faq" aria-labelledby="faq-title" />
</main>
```

Use `<video controls playsInline>` for the real demo, a native `<table>` for the comparison on wide screens, and `<details>` / `<summary>` for FAQs. Render the hardware section with a customer-value-first sentence followed by an accessible disclosure for each technical component. The final form requires name, email, and city, keeps values on failure, writes field-level errors in `aria-live="polite"` regions, and replaces the form with the interest-only confirmation after valid submission.

Set `app/page.tsx` to this exact route composition:

```tsx
import { AcbossLanding } from "./components/acboss-landing";

export default function Page() {
  return <AcbossLanding />;
}
```

- [ ] **Step 4: Run the component tests to verify they pass**

Run:

```bash
npm run test -- app/components/acboss-landing.test.tsx
```

Expected: PASS with hero-anchor, validation, and confirmation tests.

- [ ] **Step 5: Commit the customer journey**

Run:

```bash
git add app/page.tsx app/components/acboss-landing.tsx app/components/acboss-landing.test.tsx
git commit -m "feat: add Acboss customer journey"
```

Expected: one independently testable UI-and-interaction commit.

### Task 4: Apply the everyday-comfort visual system and wire real proof assets

**Files:**
- Modify: `app/globals.css`, `app/components/acboss-landing.tsx`
- Create: `public/proof/split-ac-demo.mp4`, `public/proof/split-ac-demo-poster.webp`, `public/proof/bill-savings-redacted.webp`

**Interfaces:**
- Consumes: section IDs and content data from Task 3.
- Produces: responsive visual classes used by `AcbossLanding`, including `hero`, `proof`, `comparison`, `hardware-reveal`, `preorder`, and `reduced-motion` rules.

- [ ] **Step 1: Add a failing page-level accessibility assertion for the proof assets**

Extend `app/components/acboss-landing.test.tsx`:

```tsx
it("labels the evidence assets and discloses savings variance", () => {
  render(<AcbossLanding />);
  expect(screen.getByTitle(/acboss working with a split ac/i)).toBeVisible();
  expect(screen.getByAltText(/redacted electricity bill comparison/i)).toBeVisible();
  expect(screen.getByText(/results vary by home, weather, ac, and use/i)).toBeVisible();
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```bash
npm run test -- app/components/acboss-landing.test.tsx
```

Expected: FAIL until evidence markup, alt text, and disclaimer are present.

- [ ] **Step 3: Add only authentic evidence assets**

Place the user-supplied files at these exact paths:

```text
public/proof/split-ac-demo.mp4
public/proof/split-ac-demo-poster.webp
public/proof/bill-savings-redacted.webp
```

Before copying the bill image, inspect it and permanently redact all account numbers, personal names, postal addresses, QR codes, barcodes, and customer IDs. In the component, set the video `title` to “Acboss working with a Split AC” and set the bill image `alt` to “Redacted electricity bill comparison used in Acboss testing”.

- [ ] **Step 4: Implement the responsive visual system**

Replace starter CSS with this visual contract:

```css
:root {
  --ink: #081a33;
  --paper: #f7f3ea;
  --cool: #7ee7ff;
  --blue: #175cff;
  --sun: #ffc84a;
  --line: color-mix(in srgb, var(--ink) 14%, transparent);
}

html { scroll-behavior: smooth; }
body { background: var(--paper); color: var(--ink); }
:focus-visible { outline: 3px solid var(--blue); outline-offset: 4px; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; scroll-behavior: auto !important; transition-duration: 0.01ms !important; }
}
```

Compose the hero as large editorial type beside a CSS-built product silhouette and soft airflow gradients. Use midnight-blue proof sections for the founder story and demo, an off-white comparison section with Acboss’s column highlighted, and a carefully detailed early-build section that feels transparent rather than unfinished. At `max-width: 760px`, stack columns, make the comparison table scrollable with a visible label, and keep navigation and CTAs touch-friendly.

- [ ] **Step 5: Run the focused tests to verify proof markup and interactions pass**

Run:

```bash
npm run test
```

Expected: PASS for content guardrails and component interactions.

- [ ] **Step 6: Commit styling and proof integration**

Run:

```bash
git add app/globals.css app/components/acboss-landing.tsx app/components/acboss-landing.test.tsx public/proof
git commit -m "feat: add Acboss proof-led visual design"
```

Expected: one visual-and-evidence commit; do not commit raw unredacted utility bills.

### Task 5: Finalize metadata, social preview, build, and publish

**Files:**
- Modify: `app/layout.tsx`, `app/globals.css`
- Create: `public/og.png`

**Interfaces:**
- Consumes: finished visual system, final headline, and product media.
- Produces: deployment-ready metadata and a hosted Sites URL.

- [ ] **Step 1: Write the failing metadata test**

Create `app/layout.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { metadata } from "./layout";

describe("Acboss metadata", () => {
  it("uses product-specific title and description", () => {
    expect(metadata.title).toMatch(/Acboss/i);
    expect(metadata.description).toMatch(/autopilot/i);
  });
});
```

- [ ] **Step 2: Run the metadata test to verify it fails**

Run:

```bash
npm run test -- app/layout.test.ts
```

Expected: FAIL until `layout.tsx` exports site-specific metadata.

- [ ] **Step 3: Set final metadata and create one social card**

Update `app/layout.tsx` to export metadata like:

```ts
export const metadata = {
  title: "Acboss — Your AC, finally on autopilot",
  description: "More comfort. Less energy. Zero manual fiddling.",
};
```

After the visual direction and copy are stable, make exactly one image-generation request for a 1200×630 social card. It must use the Acboss palette and the exact hero language, include the product silhouette, and be legible at unfurl size. Inspect it; retry once only if unusable. Save a valid result at `public/og.png`, then add Open Graph and X image metadata using the request host’s absolute URL.

- [ ] **Step 4: Run all tests and the production build**

Run:

```bash
npm run test
npm run build
```

Expected: every test passes and the deployment build completes with no TypeScript, asset, or metadata errors.

- [ ] **Step 5: Perform the final manual acceptance check**

Verify at desktop and narrow mobile widths:

```text
• Hero actions reach founder story and demo, never pre-order.
• Navigation and final pre-order links reach the pre-order section.
• Demo video plays, has an accurate title/poster, and proof order is founder story → demo → evidence.
• Savings bill is fully redacted and disclaimer is visible.
• Comparison calls Acboss intelligent edge-AI control without false competitor or Matter-certification claims.
• Hardware reveal makes each acronym understandable and discloses early-unit / 3D-printed status.
• Form has keyboard focus, reports each invalid field, preserves entries, and confirms interest without implying payment.
• No clipped copy, overlapping controls, or horizontal overflow.
```

- [ ] **Step 6: Commit and host**

Run:

```bash
git add app/layout.tsx app/layout.test.ts app/globals.css public/og.png
git commit -m "feat: finalize Acboss launch site"
```

Then use the Sites hosting workflow to publish the successful build. Expected: a private deployed Sites URL to share with the user.

## Self-Review

### Spec coverage

- Customer-first, one-page journey: Task 3.
- Hero, founder story, demo-first proof, savings evidence, comparison, hardware reveal, FAQ, and final pre-order: Tasks 2–4.
- Pre-order is available but not hero-primary: Task 3 tests and Task 5 manual acceptance check.
- Early handmade hardware, 3D-printed disclosure, ESP32-C5, presence sensor, IR learning, Sensirion, and cautious Matter wording: Task 2 content plus Task 4 display.
- Savings cap, evidence redaction, medical-language guardrail, and claim quality: Task 2 tests, Task 4 asset step, Task 5 acceptance check.
- Accessibility, reduced motion, responsive handling, build, social preview, and hosting: Tasks 3–5.

### Placeholder and consistency check

The plan supplies concrete file names, component interfaces, assertions, commands, and acceptance checks. The only external dependencies are the user-owned demo and bill evidence, whose required final locations and redaction treatment are explicit. `siteContent`, `AcbossLanding`, `ComparisonRow`, and `HardwareDetail` use the same names across all tasks.
