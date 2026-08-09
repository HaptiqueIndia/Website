# AC Boss Product Page Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the AC Boss product-detail page around the supplied reference page's product-story sequence while preserving original AC Boss visual identity, copy, assets, and interactions.

**Architecture:** Keep the static-site model: `product-details.html` owns semantic content and section order, `style.css` owns the page-specific visual system and responsive rules, and `script.js` owns reusable gallery and accordion behaviour. Replace the current sales-template sections with an image-led product narrative: hero, benefits, alternating feature stories, compatibility/proof, FAQ, and a truthful final CTA.

**Tech Stack:** Semantic HTML5, CSS custom properties/grid/flexbox, vanilla JavaScript, existing AC Boss raster assets.

## Global Constraints

- Use original AC Boss copy, selectors, CSS, and artwork; do not copy tado° code, text, logos, or assets.
- Use the canonical black AC Boss controller in every product view.
- Use `assets/acboss-night-hero-v1.png` for the wall-mounted visual and `assets/acboss-technical-cutaway-v1.png` only with an illustrative-technology caption.
- Do not present a real order, price, warranty, dispatch, return, compatibility, or integration claim unless it is supported by the project.
- Preserve keyboard access, visible focus styles, `prefers-reduced-motion`, and a usable narrow-screen layout.

---

### Task 1: Replace the product-detail markup and content hierarchy

**Files:**

- Modify: `product-details.html:7-426`
- Test: structural assertions run against `product-details.html`

**Interfaces:**

- Consumes: existing shared header/footer conventions and assets in `assets/`.
- Produces: stable section IDs `product-hero`, `benefits`, `comfort-story`, `mounting`, `technology`, `compatibility`, `faq`, and `interest` for navigation, CSS, and JavaScript.

- [ ] **Step 1: Write the failing structural check**

```bash
node --input-type=module -e "import fs from 'node:fs'; const html = fs.readFileSync('product-details.html', 'utf8'); for (const id of ['product-hero','benefits','comfort-story','mounting','technology','compatibility','faq','interest']) { if (!html.includes('id=\\\"' + id + '\\\"')) throw new Error('missing section: ' + id); }"
```

Expected: FAIL because the current page does not contain the new section IDs.

- [ ] **Step 2: Rebuild the document structure**

Replace the current breadcrumb, commerce hero, editions, protocol banner, data sheet, guarantee grid, and gradient conversion banner with the following original AC Boss sequence:

```html
<section class="ac-product-hero" id="product-hero"><div><p>AC Boss</p><h1>Sleep comfort, right where you sleep.</h1><a href="#mounting">See how it mounts</a></div><figure><img src="assets/acboss-night-hero-v1.png" alt="AC Boss mounted on a bedroom wall"></figure></section>
<section class="ac-benefits" id="benefits"><h2>Made for a calmer night</h2><div class="ac-benefit-grid"><article><h3>Comfort at bed level</h3></article><article><h3>Place it your way</h3></article><article><h3>Quiet local control</h3></article></div></section>
<section class="ac-story ac-story--comfort" id="comfort-story"><div><h2>Comfort follows you, not the ceiling.</h2></div><figure><img src="assets/acboss-product-pebble-vector.jpg" alt="Black AC Boss controller"></figure></section>
<section class="ac-story ac-story--mount" id="mounting"><figure><img src="assets/acboss-night-hero-v1.png" alt="AC Boss mounted on a bedroom wall"></figure><div><h2>Mount it where it matters.</h2></div></section>
<section class="ac-story ac-story--technology" id="technology"><div><h2>Thoughtful technology, kept out of sight.</h2><p>Illustrative technology view. Internal layout may change before production.</p></div><figure><img src="assets/acboss-technical-cutaway-v1.png" alt="Illustrative AC Boss technical cutaway"></figure></section>
<section class="ac-compatibility" id="compatibility"><h2>Designed around the AC you already have.</h2><p>Talk to us about your room and split AC setup.</p></section>
<section class="ac-faq" id="faq"><h2>Questions, answered simply.</h2><details><summary>Where can I place AC Boss?</summary><p>Place it on a bedside surface or use the wall-mount option.</p></details></section>
<section class="ac-interest" id="interest"><h2>Bring calmer comfort to your room.</h2><a href="mailto:hello@acboss.com">Talk to us about compatibility</a></section>
```

Use the wall-mounted render in the hero and mounting story, the canonical black product visual in the comfort story, and the technical cutaway with the text `Illustrative technology view. Internal layout may change before production.` Use `mailto:hello@acboss.com` with the label `Talk to us about compatibility` instead of a reservation/order flow.

- [ ] **Step 3: Write original customer copy**

Use concise customer language for three benefits: sleep comfort at bed level, simple placement, and quiet local control. Move technical specifications into a collapsed `details` block labelled `Technical details`; remove unverified numbers, certifications, named integrations, shipping, price, warranty, and returns claims.

- [ ] **Step 4: Verify structure and assets**

```bash
node --input-type=module -e "import fs from 'node:fs'; const html = fs.readFileSync('product-details.html', 'utf8'); for (const id of ['product-hero','benefits','comfort-story','mounting','technology','compatibility','faq','interest']) { if (!html.includes('id=\\\"' + id + '\\\"')) throw new Error('missing section: ' + id); } for (const asset of ['assets/acboss-night-hero-v1.png','assets/acboss-technical-cutaway-v1.png']) { if (!html.includes(asset)) throw new Error('missing asset: ' + asset); } if (html.includes('CORAL') || html.includes('tado')) throw new Error('reference branding leaked into page');"
git diff --check -- product-details.html
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add product-details.html
git commit -m "feat: rebuild AC Boss product page structure"
```

### Task 2: Establish the original AC Boss product-page visual system

**Files:**

- Modify: `style.css:1360-1770`
- Test: CSS token and responsive-rule assertions run against `style.css`

**Interfaces:**

- Consumes: the section and class names produced by Task 1.
- Produces: the `ac-*` component rules and responsive presentation consumed by the final static page.

- [ ] **Step 1: Write the failing visual-system check**

```bash
node --input-type=module -e "import fs from 'node:fs'; const css = fs.readFileSync('style.css', 'utf8'); for (const selector of ['.ac-product-hero','.ac-benefits','.ac-story','.ac-faq','@media (prefers-reduced-motion: reduce)']) { if (!css.includes(selector)) throw new Error('missing rule: ' + selector); }"
```

Expected: FAIL because the new product-page component system does not exist.

- [ ] **Step 2: Replace the legacy product-detail CSS**

Remove the legacy `Product Details Page (Tado-inspired Clean Aesthetics)` block and add scoped `ac-*` rules. Use warm off-white surfaces, charcoal type, subtle warm-grey dividing lines, and a restrained coral action color. Build an image-led hero with generous vertical breathing room, a three-column benefit band that becomes one column on mobile, alternating two-column stories, a dark technology panel, and a low-density FAQ/interest close. Keep global `index.html` styles intact.

- [ ] **Step 3: Add responsive and motion safeguards**

```css
@media (max-width: 760px) {
  .ac-product-hero,
  .ac-story { grid-template-columns: 1fr; }
  .ac-benefit-grid { grid-template-columns: 1fr; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] **Step 4: Verify visual-system scope**

```bash
node --input-type=module -e "import fs from 'node:fs'; const css = fs.readFileSync('style.css', 'utf8'); for (const selector of ['.ac-product-hero','.ac-benefits','.ac-story','.ac-faq','@media (prefers-reduced-motion: reduce)']) { if (!css.includes(selector)) throw new Error('missing rule: ' + selector); } if (css.includes('tado')) throw new Error('reference brand leaked into CSS');"
git diff --check -- style.css
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add style.css
git commit -m "feat: style AC Boss product story page"
```

### Task 3: Add accessible gallery and disclosure interactions

**Files:**

- Modify: `product-details.html:product gallery and FAQ markup`
- Modify: `script.js:1-20 and product interaction helpers`
- Test: static JavaScript and markup assertions

**Interfaces:**

- Consumes: gallery buttons using `data-product-src` and `data-product-alt`, plus native `details` FAQ elements.
- Produces: `initProductGallery()` that updates `#mainProductImg`, selection semantics, and alt text without inline handlers.

- [ ] **Step 1: Write the failing interaction contract check**

```bash
node --input-type=module -e "import fs from 'node:fs'; const html = fs.readFileSync('product-details.html', 'utf8'); const js = fs.readFileSync('script.js', 'utf8'); if (!html.includes('data-product-src')) throw new Error('gallery data attributes missing'); if (html.includes('onclick=\\\"switchProductImg')) throw new Error('inline gallery handler remains'); if (!js.includes('function initProductGallery')) throw new Error('gallery initializer missing');"
```

Expected: FAIL because the current gallery uses inline `switchProductImg()` handlers.

- [ ] **Step 2: Implement the gallery initializer**

Replace inline gallery handlers with labelled `<button type="button" data-product-src="assets/acboss-night-hero-v1.png" data-product-alt="AC Boss mounted on a bedroom wall" aria-pressed="true">` controls. Add the following initializer to `script.js` and call it from `DOMContentLoaded`:

```js
function initProductGallery() {
  const image = document.getElementById('mainProductImg');
  const buttons = document.querySelectorAll('[data-product-src]');
  if (!image || !buttons.length) return;

  buttons.forEach((button) => button.addEventListener('click', () => {
    image.src = button.dataset.productSrc;
    image.alt = button.dataset.productAlt;
    buttons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
  }));
}
```

- [ ] **Step 3: Use native disclosures**

Use `details` and `summary` for FAQs and technical details. Do not add custom accordion state. Add visible summary focus styling to the page CSS.

- [ ] **Step 4: Run interaction and syntax checks**

```bash
node --input-type=module -e "import fs from 'node:fs'; const html = fs.readFileSync('product-details.html', 'utf8'); const js = fs.readFileSync('script.js', 'utf8'); if (!html.includes('data-product-src')) throw new Error('gallery data attributes missing'); if (html.includes('onclick=\\\"switchProductImg')) throw new Error('inline gallery handler remains'); if (!js.includes('function initProductGallery')) throw new Error('gallery initializer missing');"
node --check script.js
git diff --check -- product-details.html style.css script.js
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add product-details.html style.css script.js
git commit -m "feat: add accessible product interactions"
```

## Self-Review

- **Spec coverage:** Task 1 implements the reference-derived sequence and original content; Task 2 implements original visual pacing and responsive motion rules; Task 3 covers gallery, disclosure, and accessible interaction requirements.
- **Placeholder scan:** No unresolved implementation markers or undefined steps remain.
- **Type consistency:** Task 1 defines the markup interfaces that Task 2 styles and Task 3 reads. The gallery contract consistently uses `data-product-src`, `data-product-alt`, `#mainProductImg`, and `initProductGallery()`.
