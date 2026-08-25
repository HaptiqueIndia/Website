# ROOT Technical Whitepaper Design

## Purpose

Create a developer-gated technical whitepaper page for ROOT that explains the product's room-level, local-first approach to split-AC comfort. The page should help engineering reviewers, partners, and early collaborators understand the system without exposing the entire development site publicly or presenting unverified claims as established results.

## Goals

- Explain the problem ROOT is intended to address: split-AC control is commonly based on a wall or ceiling reference rather than the climate experienced near a bed, couch, or occupant.
- Describe the intended local control loop in plain engineering language.
- Distinguish implemented behavior, prototype behavior, design targets, and work requiring validation.
- Document the role of room sensing, human-presence sensing, Bluetooth setup, infrared learning, and local AC control.
- Provide a concise evaluation framework that can later be populated with measured results.
- Include the supplied company, Panasonic Ignition, Acceleration Award, and patent-pending context without inventing legal or technical details.
- Keep the page available for local/developer review while the production site remains behind the coming-soon gate.

## Non-goals

- Do not create a downloadable PDF or document-generation pipeline in this phase.
- Do not publish clinical, medical, therapeutic, or disease-prevention claims.
- Do not state sensor accuracy, PMV computation, compatibility counts, performance improvements, or reliability results as facts without supporting test evidence.
- Do not expose pinout tables, proprietary implementation details, credentials, or unpublished filing information.
- Do not change the public launch-gate behavior.
- Do not add a backend, analytics system, CMS, or authentication layer.

## Proposed page

Add `whitepaper.html` as a semantic, static page using the existing ROOT navigation and typography. The page will use a technical editorial tone: compact labels, readable paragraphs, restrained diagrams or existing product imagery, and explicit status labels for evidence maturity.

### Page sequence

1. **Cover and abstract**
   - Title: `ROOT: A local architecture for room-level AC comfort`
   - Short abstract describing the design thesis, not a performance promise.
   - Status marker: `Technical concept paper / developer preview`.

2. **The room-level problem**
   - Explain why a split AC's built-in temperature reference may not represent the conditions near the person.
   - Use bed-level and couch-level language already established on the site.

3. **System architecture**
   - Present a four-stage loop: sense the room, estimate occupancy/context, decide locally, transmit an IR adjustment.
   - Use existing technical-cutaway and product assets as illustrative visuals.
   - Label visuals as conceptual or illustrative where they do not represent verified hardware.

4. **Connectivity and control boundary**
   - Explain Bluetooth as a setup/proximity pathway where applicable.
   - Explain that the intended core control path runs on the device without an active Wi-Fi network or external cloud service.
   - Avoid claiming that every future feature is available offline.

5. **Sensing and infrared interface**
   - Describe temperature/humidity sensing, presence sensing, IR learning, and wide-angle IR transmission as system elements or current development targets according to evidence status.
   - Omit pinouts and low-level identifiers from the published page.

6. **Placement and room coverage**
   - Explain tabletop, nightstand, couch-side, and wall-mount placement.
   - State that placement affects sensing quality and line-of-sight/coverage assumptions.

7. **Evaluation methodology**
   - Define future measurements: local temperature stability, humidity behavior, presence response, IR compatibility, offline operation, setup time, and power behavior.
   - Provide clearly labeled `planned evaluation` panels instead of presenting unmeasured results.

8. **Limitations and safety boundary**
   - State that ROOT is not a medical device and does not diagnose, prevent, or treat illness.
   - Avoid promising benefits for children, older adults, or people with arthritis; describe those as comfort-design considerations requiring user research and validation.
   - State that split-AC compatibility and performance depend on hardware, room geometry, placement, and operating conditions.

9. **Company and disclosure**
   - Identify Haptique Electronics Pvt. Ltd. as the company behind ROOT.
   - Include the supplied Panasonic Ignition affiliation and `Acceleration Award at Panasonic Ignition, 2025` wording.
   - State that work around local comfort control and room-level sensing is patent pending, without a filing number or legal conclusion.

10. **Roadmap and contact**
    - Summarize the next evidence milestones.
    - Link to the existing product page and developer/local sitemap contact path.

## Evidence language

The page must use one of these labels when describing product behavior:

- `Current site behavior` — supported by the current static implementation.
- `Prototype direction` — represented in the current product concept or interaction but not independently verified.
- `Design target` — an intended behavior or engineering objective.
- `Planned evaluation` — a measurement or validation step that has not yet been reported.

The whitepaper must not convert copy found in the existing site into test evidence automatically. Existing site claims are source material for the draft, not proof of measured performance.

## Architecture and integration

- Keep the existing static HTML/CSS/JavaScript architecture.
- Add page-scoped `ac-whitepaper-*` selectors to `style.css` only.
- Add the whitepaper route to local sitemap/company navigation where it is useful for developer review.
- Do not modify `site-gate.js` to make the page public. The existing localhost allowance and production coming-soon redirect remain the access boundary.
- Extend the existing Node assertion test or add a focused `tests/whitepaper.test.mjs` contract test. The test must verify the title, required sections, evidence labels, non-medical disclaimer, company disclosure, and presence of `site-gate.js` on the page.
- Use existing assets unless a diagram cannot be communicated clearly without a new asset. No image-generation step is required for the first whitepaper version.

## Accessibility and responsive behavior

- Use one `h1`, ordered `h2` sections, semantic lists, and descriptive image alt text.
- Keep text within readable line lengths and preserve visible keyboard focus styles.
- Collapse the architecture/evaluation layouts to a single column on narrow screens.
- Avoid horizontal overflow except for intentionally contained technical tables, and omit such tables in this first version.
- Respect the existing reduced-motion and page-gate behavior.

## Verification

- Run the focused whitepaper contract test.
- Run `node --check script.js` if shared JavaScript changes are made.
- Run `git diff --check`.
- Start the local server and confirm `whitepaper.html` returns HTTP 200.
- Confirm the public gate still redirects the page when evaluated on a non-local host through the existing gate contract.
- Review the final copy for unsupported medical, legal, patent, accuracy, and performance claims.

## Future publication path

Once ROOT has measured data and approved technical language, the page can be converted into a public-facing technical brief or exported into a PDF. That future phase should add dated revision information, authorship, references, test conditions, measured results, and a clear distinction between prototype data and production specifications.
