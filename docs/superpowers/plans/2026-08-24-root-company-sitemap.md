# ROOT Company Sitemap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the homepage’s top-level “Talk to us” email tab with a footer-linked company sitemap page for Heptic Electronics Pvt. Ltd., including company context, Panasonic Ignition affiliation, patent-pending information, social/community links, and an email handoff form.

**Architecture:** Keep the existing static-site architecture. Add one standalone `sitemap.html` page using the existing ROOT navigation, typography, color tokens, and footer conventions. Use a client-side `mailto:` handoff for the message form because the repository has no server-side contact endpoint.

**Tech Stack:** Semantic HTML, existing `style.css`, existing `script.js`, vanilla JavaScript, Node’s built-in `assert` module for regression checks.

**Spec:** User-approved sitemap/company/contact direction from the 2026-08-24 request.

## Global Constraints

- Remove “Talk to us” from the homepage primary navigation.
- Keep Discord as the real-time communication option.
- Use “patent pending” without inventing a filing number or legal claim.
- Describe Panasonic Ignition affiliation only as supplied by the user.
- Preserve unrelated working-tree files and existing site routes.
- Keep the contact form transparent: it opens the visitor’s email client with a prepared message.

---

### Task 1: Add regression checks for the sitemap contract

**Files:**
- Create: `tests/sitemap.test.mjs`

**Interfaces:**
- Consumes: `index.html`, `sitemap.html`, and `style.css` from the repository root.
- Produces: a zero-exit Node check that guards navigation, sitemap content, and contact-form behavior.

- [ ] **Step 1: Write assertions that initially fail**

  Assert that `index.html` has no primary-navigation link whose visible text is `Talk to us` and has a footer link to `sitemap.html`. Assert that `sitemap.html` contains `Heptic Electronics Pvt. Ltd.`, `Panasonic Ignition`, `Patent pending`, a Discord link, a form with `name`, `email`, and `message` controls, and a `mailto:` handoff.

- [ ] **Step 2: Run the check to verify the expected failure**

  Run: `node tests/sitemap.test.mjs`

  Expected: FAIL because `sitemap.html` does not yet exist and the homepage still contains the old Talk to us link.

---

### Task 2: Build the company sitemap page

**Files:**
- Create: `sitemap.html`
- Modify: `style.css`
- Modify: `script.js`

**Interfaces:**
- Consumes: the existing `ac-product-page`, `ac-nav`, `ac-footer`, `ac-eyebrow`, `ac-button`, and typography conventions.
- Produces: a responsive public page at `/sitemap.html` with sections for company, site map, IP, community/socials, and contact.

- [ ] **Step 1: Add semantic page structure**

  Create a page with a ROOT wordmark, links back to Home, Product, About, and the relevant product anchors. Use a hero titled “A clearer map of what we’re building.” Follow with:

  - Company: Heptic Electronics Pvt. Ltd., with a concise description of ROOT.
  - Affiliation: Panasonic Ignition, described as an affiliation without extra unsupported details.
  - Site map: grouped links for ROOT, company, and community/contact destinations.
  - Intellectual property: “Patent pending” and a brief statement that technical details will be shared as appropriate.
  - Community and socials: Discord as the primary live channel and a small, clearly labeled social-links group using existing known URLs only.
  - Contact: accessible name, email, and message fields with a submit button and a note that submission opens the visitor’s email client.

- [ ] **Step 2: Add the email handoff behavior**

  In `script.js`, attach behavior to the sitemap form only. On submit, validate through native required fields, URL-encode the subject and body, and navigate to `mailto:info@get-root.in`. Include the visitor’s name, email, and message in the body. Do not send data to an invented endpoint.

- [ ] **Step 3: Style the page responsively**

  Add scoped `ac-sitemap-*` styles to `style.css`: an asymmetric hero, grouped sitemap lists, a restrained affiliation/IP band, and a two-column contact region that collapses cleanly on narrow screens. Reuse existing ROOT colors, borders, buttons, and spacing. Keep body copy within readable line lengths and provide visible focus styles.

- [ ] **Step 4: Run the regression check**

  Run: `node tests/sitemap.test.mjs`

  Expected: PASS.

---

### Task 3: Update navigation and footer entry points

**Files:**
- Modify: `index.html`
- Modify: `about.html`
- Modify: `product-details.html`

**Interfaces:**
- Consumes: `sitemap.html` from Task 2.
- Produces: consistent footer access to the sitemap and no homepage top-nav “Talk to us” email tab.

- [ ] **Step 1: Remove the homepage primary-navigation email tab**

  Delete only the `Talk to us` list item from `index.html`; preserve Product, Comfort, How it works, About, and Discord.

- [ ] **Step 2: Add sitemap footer links**

  Add `Sitemap` to the homepage, About, product-details, and sitemap footer link groups. Keep existing compatibility email actions on the product page because they are contextual product enquiries, not the removed top-level tab.

- [ ] **Step 3: Re-run the regression check**

  Run: `node tests/sitemap.test.mjs`

  Expected: PASS.

---

### Task 4: Verify the shipped static site

**Files:**
- Verify: `index.html`, `about.html`, `product-details.html`, `sitemap.html`, `style.css`, `script.js`, `tests/sitemap.test.mjs`

**Interfaces:**
- Consumes: all implementation changes from Tasks 1–3.
- Produces: checked markup, scripts, whitespace, and responsive page availability.

- [ ] **Step 1: Run static checks**

  Run: `node tests/sitemap.test.mjs`

  Run: `node --check script.js`

  Run: `git diff --check`

- [ ] **Step 2: Start the local server if needed and request the page**

  Run: `python3 -m http.server 8000`

  Verify: `curl -I http://localhost:8000/sitemap.html` returns HTTP 200.

- [ ] **Step 3: Inspect the final diff**

  Run: `git diff --stat` and `git diff -- index.html about.html product-details.html sitemap.html style.css script.js tests/sitemap.test.mjs`

  Confirm that only the requested sitemap, navigation, footer, contact behavior, and regression-check changes are present.
