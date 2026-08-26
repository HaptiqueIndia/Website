# ROOT Technical Concept Paper Publication Design

## Purpose

Create a canonical engineering concept paper for local or explicitly authorized review that explains ROOT's proposed room-level, local-first approach to split-AC comfort. The primary publication is a stable, print-ready PDF generated from an editable DOCX source. A companion HTML reader may help engineering reviewers, partners, and early collaborators navigate the same material, but it is not the authoritative publication.

Before public-release approval, the paper and its distinctive content must not be included in or returned by the public production origin. The existing client-side coming-soon redirect is launch-screen behavior, not an authorization or confidentiality control.

## Publication status

- Public label: `Technical concept paper / developer preview`.
- Canonical artifact: versioned PDF.
- Editable publication source: DOCX with matching revision metadata and content.
- Companion artifact: HTML reader, explicitly subordinate to the PDF.
- Default access model: local-only review.
- Optional remote review: a separate preview origin protected by hosting- or edge-layer authentication before the response body is returned.
- Public production status: excluded until the release gate in this specification is satisfied.
- No artifact may be described as a measured-results whitepaper while it contains no approved prototype results.
- The PDF, DOCX, and HTML must carry the same document ID, revision, issue date, evidence cutoff, publication status, and material claims.

## Publication hierarchy

1. `output/pdf/ROOT-Technical-Concept-Paper-D0.1.pdf` is the canonical review artifact.
2. `output/docx/ROOT-Technical-Concept-Paper-D0.1.docx` is the editable source used to revise the canonical artifact.
3. `whitepaper.html` is a companion web reader. It must identify itself as a web edition and direct reviewers to the canonical revision when downloads are later authorized.
4. The PDF and DOCX remain local-only until the public-release gate is satisfied. They must be excluded from `dist/` under the same boundary as the HTML reader.

The canonical paper is an engineering publication, not a product microsite. Its credibility comes from restrained document design, explicit assumptions and evidence states, reproducible methods, complete limitations, and stable pagination.

## Goals

- Explain the problem ROOT is intended to address: a split AC's return-air reference may not represent conditions at an occupied location such as a bed, couch, or desk.
- Describe the intended local control loop in plain engineering language.
- Separate cited HVAC background from claims about ROOT.
- Distinguish observed prototype behavior, hypotheses and design targets, and planned evaluations.
- Document the proposed roles of climate sensing, presence sensing, Bluetooth setup or proximity, infrared learning, and local AC control.
- Provide a reproducible evaluation framework that can later be populated with measured results.
- Include company, Panasonic Ignition, and patent-status context only where the identity, wording, and supporting records are verified.
- Keep the paper available locally and, if configured, through an authenticated preview origin while excluding it and all links to it from the public production artifact.

## Identity source of truth

- Haptique Electronics Pvt. Ltd. is the legal company developing ROOT.
- ROOT is a product and brand, not a legal entity.
- Panasonic recognition may be attributed only to one exact entity and award-category string verified against a primary Panasonic source.
- Until that exact entity and the Cantata-Haptique relationship are documented internally and approved for publication, omit Panasonic recognition from the paper rather than choosing between `Cantata`, `Cantata CS`, Haptique Electronics, or ROOT.
- Do not use `affiliated with Panasonic Ignition`, `Acceleration Award`, or wording that implies Panasonic endorsement, certification, investment, or co-development of ROOT.
- Founder titles must refer to a verified company role, not `Co-founder of ROOT`.

## Non-goals

- Do not create a public download route or include the PDF or DOCX in the production artifact in this phase.
- Do not publish clinical, medical, therapeutic, disease-prevention, health-monitoring, vital-sign, sleep-monitoring, or safety-critical claims.
- Do not state sensor accuracy, PMV computation, compatibility counts, setup time, coverage, performance improvements, energy savings, or reliability results as facts without supporting test evidence.
- Do not expose pinout tables, proprietary implementation details, credentials, security-sensitive configuration, or unpublished filing information.
- Do not change the existing coming-soon experience for ordinary public-site routes or use it as the paper's security boundary.
- Do not add application-level authentication, a custom backend, analytics, a CMS, or a product data service.
- Do not treat an unguessable URL, `robots.txt`, `noindex`, rendered imagery, simulation, or website copy as confidentiality or product evidence.

## Preview access and publication boundary

- Confidentiality means an unauthenticated request to the public production origin must not receive any concept-paper content, regardless of JavaScript execution.
- The default implementation is local-only review plus a deterministic `dist/` production artifact that excludes `whitepaper.html`.
- Add `scripts/build-production.mjs` as the required production build entry point. It must create a clean `dist/` directory from an explicit allowlist containing only the approved public HTML pages, `style.css`, `script.js`, `site-gate.js`, and referenced files under `assets/`. It must never copy `whitepaper.html`, developer-only navigation, source maps containing paper content, repository documentation, or unlisted root files.
- Configure production hosting to publish only `dist/`. Adding `whitepaper.html` to a deployable source tree is blocked until the production hosting entry point is confirmed to be `dist/` and the deployed artifact matches the locally tested build output.
- If remote review is required, deploy the static page only to a separate preview origin protected by hosting- or edge-layer authentication. Authentication must be enforced before the response body is returned.
- The public production artifact must exclude `whitepaper.html`, links to it, developer-only navigation, source maps containing its content, and whitepaper-specific downloadable artifacts.
- Do not add a whitepaper link to shared production navigation. A development-only index may link to it only if that index is also excluded from production.
- Add `noindex,nofollow,noarchive,nosnippet` metadata and an equivalent `X-Robots-Tag` header where supported for a remote preview. These controls are defense in depth, not access control.
- Use `Cache-Control: private, no-store` for a remote authenticated preview where supported.
- If the production publish root and preview protection cannot be identified and verified, the paper must remain local-only and must not be deployed.

## Canonical document design

Create an A4 technical paper of approximately 12-16 pages, allowing the final page count to follow content rather than forcing filler or unsafe compression.

### Visual system

- Use a restrained engineering-report register: white paper, near-black text, neutral grey rules, and ROOT coral only for small navigational or status accents.
- Use a highly readable sans-serif family available in the bundled document runtime. Body copy should render at approximately 9.5-10.5 pt with comfortable leading; headings should be compact and sober rather than oversized or promotional.
- Use approximately 18-22 mm page margins, with a slightly wider inner margin only if binding requires it.
- Use running headers containing the abbreviated title and revision, and footers containing the document ID, publication status, and `Page X of Y`.
- Do not use full-bleed product photography, oversized marketing headlines, decorative gradients, glass effects, promotional feature cards, or landing-page calls to action.
- Use thin rules, whitespace, numbered headings, figure captions, table captions, notes, and definition lists to establish hierarchy.
- Ensure black-and-white printing remains legible. Evidence status and figure meaning must never depend on color alone.

### Front matter

1. Cover with title, subtitle, document ID, revision, publication status, owner, reviewer, issue date, and evidence cutoff.
2. Abstract of approximately 150-220 words that states the design thesis, scope, and absence of measured product-performance results.
3. Document-control and revision table.
4. Static table of contents with page numbers in the canonical PDF.
5. Nomenclature or abbreviations list covering AC, IR, RSSI, HVAC, and any other abbreviation used more than once.

### Technical body

Use numbered headings and preserve the substantive sequence defined below. Each section must begin with its scope or question, then present technical content, evidence classification, assumptions, and limitations where applicable. Figures and tables must be numbered independently and referenced from the prose.

Architecture drawings should use simple vector geometry where practical. Product imagery may appear only as a compact, captioned illustrative figure. Protocol matrices should use repeated table headers, intentional column widths, and sufficient cell padding; dense material may move to an appendix rather than shrinking below a readable size.

### Back matter

- Limitations, intended use, safety boundary, and privacy boundary remain part of the technical body rather than promotional fine print.
- Include numbered references using one consistent citation style with stable URLs or DOIs.
- Include a claim register summary or appendix mapping claim IDs to evidence status and evidence/reference IDs.
- Include a planned-evaluation appendix if the full protocol matrix would interrupt the main narrative.
- End with revision history and developer contact information.

## Companion web reader

Retain `whitepaper.html` as a semantic static source page for local or authorized preview. It may use the existing ROOT company-page typography and navigation patterns, with page-scoped `ac-whitepaper-*` selectors, but it must describe itself as the companion web edition rather than the canonical paper. Its purpose is on-screen reading and navigation, not replacement of document conventions.

Avoid a repeated grid of identical status cards. Use structured section rows, figures, definition lists, and claim annotations so evidence maturity remains legible without overwhelming the narrative.

### Publication sequence

1. **Cover, abstract, and document control**
   - Title: `ROOT: A local architecture for room-level AC comfort`.
   - Short abstract describing the design thesis, not a performance promise.
   - Status marker: `Technical concept paper / developer preview`.
   - Show document ID, revision, publication status, owner or author, technical reviewer, issued date, last-reviewed date, evidence cutoff date, applicable prototype hardware revision, applicable firmware revision, and a revision-history reference appropriate to each format.
   - Use `Not yet assigned` rather than silently omitting an unavailable document-control field.

2. **The room-level problem**
   - Explain qualitatively why a split AC's built-in return-air reference may not represent conditions near an occupant.
   - Distinguish cited HVAC background from the ROOT design hypothesis.
   - Use bed-level, couch-level, and occupied-location language without implying that every room has the same thermal gradient.
   - Any numerical temperature difference, return-air behavior, or occupant-zone example requires an inline citation and stated test conditions.

3. **System architecture**
   - Present a four-stage loop: sense the room, estimate occupancy or context, decide locally, transmit an IR adjustment.
   - For each stage, state whether it is observed on an identified prototype revision or remains a hypothesis or design target.
   - Caption unverified diagrams `Conceptual architecture, not a measured result`.
   - Caption rendered or cutaway product imagery as illustrative. Imagery is not evidence of component presence, layout, or production construction.

4. **Connectivity, data, and control boundary**
   - Define separately: initial setup transport, remote-learning flow, configuration storage, sensing path, decision path, IR transmission path, optional network features, and behavior after loss of Wi-Fi or internet.
   - Explain Bluetooth as a proposed setup or coarse-proximity pathway only where applicable.
   - Define what identifiers, signal-strength values, configuration, or event data may be processed; where processing occurs; whether anything is stored or shared; retention and deletion behavior; factory-reset behavior; platform permissions; and whether GPS or another location source is used.
   - State that Bluetooth received signal strength is environment-dependent and must not be the sole input for a safety-relevant or irreversible action.
   - `Local`, `offline`, and `100% local` may be used only for a specifically tested boundary and prototype revision. They must not imply that every setup, app, update, support, or future feature is offline, that no personal data is processed, or that the system is immune to power, sensor, firmware, hardware, or AC failure.

5. **Sensing and infrared interface**
   - Describe temperature and humidity sensing, presence sensing, IR learning, and wide-angle IR transmission according to their evidence status.
   - Use `presence sensing`, not `breathing sense`, respiration monitoring, sleep monitoring, or health monitoring.
   - Treat sensor part specifications, display resolution, simulation parameters, and marketing copy as design inputs, not measured system accuracy.
   - Omit pinouts, low-level identifiers, and security-sensitive implementation detail.

6. **Placement and room coverage**
   - Explain tabletop, nightstand, couch-side, desk-side, and wall-mount concepts without implying equivalent sensing quality.
   - State that placement affects sampled conditions, obstruction, airflow exposure, line of sight, IR reach, mounting stability, and presence-detection behavior.
   - Avoid `perfect coverage`, `any wall`, `universal`, or equivalent categorical language.

7. **Evaluation methodology**
   - Publish a planned protocol matrix. Each evaluation must identify the prototype and firmware revision, room or bench conditions, comparator and ground truth, sample interval, repeated trials, primary outcome, secondary outcomes, acceptance criterion fixed before testing, exclusions and missing-data handling, uncertainty, and retained evidence artifact.
   - Report trial counts, negative results, protocol deviations, raw and derived data location, and analysis version. Use confidence intervals or another justified uncertainty summary when reporting results.
   - Do not promote a simulator output to a measured result.

   Minimum planned evaluations:

   - **Climate sensing:** Co-locate ROOT with a traceable reference logger across relevant temperature and humidity conditions. Plan to report bias, mean absolute error, repeatability, sampling interval, stabilization time, and measurement uncertainty. Do not equate resolution with accuracy.
   - **Presence sensing:** Compare detections with timestamped ground truth across occupied, unoccupied, stationary, moving, obstructed, placement, and false-trigger scenarios. Plan to report sensitivity, specificity or false-positive rate, and response latency.
   - **IR interoperability:** Test a declared, stratified sample of AC brands, models, and commands over repeated trials, distances, angles, and line-of-sight conditions. Report model-level successes and failures, not universal compatibility.
   - **Offline control:** Disable Wi-Fi and internet after setup, then exercise sensing, decisions, commands, reboot, and reconnection for a stated duration. Distinguish network independence from electrical uptime and system reliability.
   - **Setup:** Observe first-time users completing a defined setup flow. Report completion rate, median and range or interquartile range, assistance, retries, and failure reasons.
   - **Power behavior:** Measure nominal and peak draw, supported input conditions, brownout and restart behavior, and recovery state using declared equipment.
   - **Room comfort stability:** Use a randomized or counterbalanced baseline-versus-ROOT comparison under recorded room geometry, placement, AC model, loads, outdoor conditions, and occupancy. Predefine occupant-zone deviation, overshoot, cycling, and humidity outcomes. Treat energy savings as out of scope unless separately metered.

8. **Limitations, privacy, and safety boundary**
   - State that ROOT is intended for general room-comfort control. It is not a medical device and is not intended to diagnose, prevent, monitor, predict, mitigate, or treat any disease, disorder, injury, disability, physiological condition, sleep condition, or vital sign.
   - Do not promise benefits for children, older adults, people with arthritis, or other vulnerable or health-defined groups. General comfort scenarios require user research and validation.
   - State that ROOT is not a safety-critical, emergency, or life-support controller.
   - Users must retain the original AC remote and access to the AC's manual controls.
   - Treat bounded setpoints, bounded command rates, visible fault indication, manual override, and a neutral fallback as design targets until implemented and tested.
   - Plan validation for sensor faults, stale or out-of-range inputs, loss of paired-device proximity, ambiguous or unsupported IR state, blocked line of sight, AC non-response, power interruption and restart, conflicting occupant preferences, mounting failure, and loss of optional connectivity.
   - Do not treat an emitted IR command as confirmed AC state unless a validated feedback mechanism exists.
   - State that compatibility and performance depend on AC hardware, room geometry, placement, obstruction, environmental conditions, power, firmware, and operating mode.

9. **Company and disclosure**
   - Identify Haptique Electronics Pvt. Ltd. as the company developing ROOT.
   - If the relationship is internally documented and approved, use one exact entity and award-category string verified against the cited primary Panasonic source, then separately explain the verified relationship to Haptique Electronics.
   - Cite the primary Panasonic source adjacent to the recognition statement.
   - State explicitly that the recognition does not imply Panasonic endorsement, certification, investment, or co-development of ROOT unless a source supports that specific relationship.
   - Patent language requires evidence of an actual filing, verified applicant or assignee, jurisdiction, current status, and counsel-approved technical scope.
   - If a filing is verified, use bounded wording such as: `A patent application has been filed concerning certain aspects of [approved technical subject]. The application is pending; no patent has been granted.`
   - If filing cannot be verified, omit `patent pending` or use `Patent application planned` only if that statement is accurate and approved.

10. **Roadmap, references, and contact**
    - Summarize the next evidence milestones without promising dates that have not been approved.
    - Include numbered references with stable URLs or DOIs and access dates where applicable.
    - Link to a maintained developer contact path.
    - Do not link to public product or company pages until the cross-site consistency gate is satisfied.

11. **Revision history**
    - Provide an anchor target for the document-control change-summary link.
    - List revision, issue date, owner or author, reviewer, evidence cutoff date, and a concise summary of material changes.

## Evidence language

Every substantive empirical technical, compatibility, reliability, privacy-behavior, or performance claim must carry exactly one evidence status:

- `Cited background`: A claim about established HVAC, sensing, human-factors, or control-system context supported by an inline citation to an independent source. It must not imply that ROOT achieved the cited result.
- `Implemented prototype behavior`: Behavior directly observed on an identified ROOT hardware and firmware revision using a dated, repeatable protocol. A website mockup, source-code path, simulation, rendered image, or component datasheet alone does not qualify.
- `Hypothesis / design target`: An intended behavior, proposed mechanism, engineering requirement, or expected benefit that has not met the prototype-evidence rule. Phrase it with `intended`, `designed to`, `target`, or `hypothesis`, not present-tense achievement language.
- `Planned evaluation`: A specified measurement or validation activity for which no result is reported.

Each empirical claim annotation must state its status, scope, applicable hardware and firmware revision, evidence or reference ID, and evidence date. Use `Not applicable` for independent cited background, and `Target revision not yet assigned` for planned work with no assigned revision. For cited background, the evidence date is the source publication date; for prototype behavior, it is the observation or test date; for a hypothesis or planned evaluation, it is the most recent review date. If no evidence record exists, classify the claim as a hypothesis or design target.

Intended-use, medical, safety, company, recognition, privacy-policy, and patent statements are controlled disclosures, not empirical evidence claims. Each controlled disclosure must identify its disclosure type, exact approved wording, source or approval record, owner, approval date, and next review date. A `Company-supplied disclosure, not independently verified` label is permitted only in the developer preview and blocks public release until replaced by a verified and approved disclosure or omitted.

Existing site copy, diagrams, UI interactions, simulated curves, marketing comparisons, renderings, and linked pages are draft source material, not product test evidence.

## Claim register and citations

- Maintain a claim register mapping each claim ID to its exact wording, evidence status, scope, evidence or reference ID, owner, review date, and superseded wording.
- Background references must include author or organization, title, publisher, publication date, stable URL or DOI, and access date where applicable.
- Prefer standards, peer-reviewed literature, manufacturer documentation, and primary institutional sources.
- Company, recognition, relationship, and patent statements require a primary public citation or the controlled-disclosure treatment defined above.
- Patent wording must be counsel-approved and must not imply grant, validity, scope, or freedom to operate.
- A numerical claim must identify its source and conditions. Otherwise, keep the statement qualitative.

## Cross-site consistency gate

Disclosure consistency applies to every page linked from the concept paper. The paper must not be released publicly alongside stronger medical, patent, Panasonic, privacy, reliability, accuracy, compatibility, coverage, setup-time, or performance claims that the paper classifies as unverified.

Before enabling public links or public access, audit `index.html`, `product-details.html`, `about.html`, `sitemap.html`, `privacy-policy.html`, shared footers, and relevant tests. Resolve or remove at least the following unsupported or ambiguous language unless evidence and approval exist:

- `Acceleration Award` and broad Panasonic `affiliation` wording.
- Any attribution of Cantata recognition to Haptique Electronics or ROOT without a documented identity relationship.
- Broad `patent pending` claims without verified filing status and bounded scope.
- Claims directed at children, older adults, arthritis, skin, breathing, sleep, health, or other medical or vulnerable-population outcomes.
- `3°C to 4°C`, `±0.1°C`, PMV, `under 2 minutes`, `100% local`, `zero outages`, `instant`, `perfect coverage`, `universal`, `fully-tested`, and comparable categorical claims.
- Synthetic curves or simulations described as prevention, performance, or measured outcomes.
- Competitor claims without named scope and primary evidence.
- Ambiguous setup language that does not distinguish Bluetooth configuration from IR remote learning.

The website privacy notice must accurately describe the `mailto:` contact handoff, hosting logs, third-party font requests, recipient categories, retention, and its scope. A separate product or companion-app privacy notice and data-flow review are required before testing Bluetooth proximity or presence features with people.

## Architecture and integration

- Author the editable canonical publication as deterministic DOCX source and export the reviewed version to PDF.
- Store final artifacts at the stable paths defined in `Publication hierarchy`; keep render PNGs, temporary office profiles, and intermediate PDFs outside the final output folders.
- The DOCX and PDF must share the same content, revision metadata, figure numbering, reference numbering, and substantive claim wording. Small pagination-driven line-wrap differences are acceptable.
- Render the DOCX through the bundled document workflow and use the emitted PDF as the canonical PDF unless a documented conversion defect requires a controlled PDF repair.
- Scrub personal document metadata that is not part of the approved authorship or company disclosure before delivery.
- Keep the companion HTML static and source-controlled, but do not make HTML the source of truth for pagination, table of contents, headers, footers, or print layout.
- Keep the source page static HTML, CSS, and JavaScript.
- Add the deterministic `scripts/build-production.mjs` entry point and publish only its clean `dist/` output. Do not publish the repository root once developer-only content exists.
- Exclude `whitepaper.html`, developer-only navigation, source maps containing its content, and whitepaper-specific downloadable artifacts from production output.
- Do not add the paper route to shared production navigation.
- Leave `site-gate.js` unchanged for the existing launch-screen experience, but do not load or test it as the paper's access control. It may remain on the local page solely for visual consistency if desired.
- Add page-scoped `ac-whitepaper-*` selectors to `style.css` only.
- Use existing assets unless a diagram cannot be communicated clearly without a new asset.
- Add a focused `tests/whitepaper.test.mjs` content contract and a separate publication-boundary test.

The content contract must verify:

- title, required sections, and document-control fields;
- all evidence-status labels and definitions;
- claim IDs and reference IDs;
- non-medical, privacy, safety, company, recognition, and patent boundaries;
- conceptual and simulation disclaimers;
- figure captions and accessible visual fallbacks;
- no broken citation or footnote targets;
- no unqualified numerical performance, accuracy, medical, `universal`, `zero outage`, `fully-tested`, or equivalent prohibited language.

The publication-boundary test must inspect the exact generated production artifact and fail if it contains `whitepaper.html`, a link to it, a source map containing its content, or a distinctive concept-paper marker.

## Accessibility and responsive behavior

- Use one `h1`, ordered `h2` sections, semantic lists, descriptive image alt text, `figure`, and `figcaption` where appropriate.
- Cap body text at approximately `65–75ch` on sufficiently wide viewports, allow naturally shorter lines on narrow screens, and preserve visible keyboard focus styles.
- Collapse architecture and evaluation layouts to a single column on narrow screens.
- Avoid horizontal overflow. If a compact protocol table is necessary, contain it in a labelled, keyboard-accessible region and provide a stacked narrow-screen treatment.
- Respect the existing reduced-motion behavior.
- Convey evidence status in visible text, not color alone, with sufficient contrast.
- Give every figure a figure number, descriptive caption, status, and source or evidence ID.
- Give charts a nearby text summary and accessible data table. Use direct labels or patterns in addition to color.
- Do not use canvas-only evidence visuals.
- Give SVG diagrams a meaningful `<title>` and `<desc>` or an equivalent adjacent explanation.
- Use unique citation and footnote link text with bidirectional backlinks.
- Make conceptual, simulated, prototype-observed, and measured visuals visually and textually distinguishable.

## Verification

- Render every DOCX page to PNG and inspect the complete page set for clipping, overlap, orphaned headings, broken tables, weak page breaks, inconsistent spacing, and unreadable captions.
- Reopen the final PDF, confirm page count and A4 page geometry, extract its text, and verify that the title, document ID, revision, required headings, figure captions, references, limitations, and revision history are present.
- Render every PDF page to PNG and inspect the complete page set. The final PDF must show correct running headers, footers, page numbering, section transitions, table continuations, and black-and-white legibility.
- Run document accessibility checks for heading structure, table headers, descriptive image alternative text, and reading order to the extent supported by DOCX/PDF tooling.
- Compare PDF and DOCX text or a normalized content manifest so no substantive section, claim ID, evidence status, reference, or controlled disclosure is lost during export.
- Confirm that PDF and DOCX filenames, internal revision metadata, cover metadata, running metadata, and revision history agree.
- Run the focused concept-paper content contract against the developer source or artifact.
- Run `node scripts/build-production.mjs` to generate the exact clean `dist/` artifact used by hosting.
- Assert that the production artifact contains neither `whitepaper.html`, links to it, source maps containing its content, nor distinctive concept-paper text.
- Serve the production artifact and issue a JavaScript-free HTTP `GET` to `/whitepaper.html`. Require a non-content response such as `404` or `410`, and assert that the body contains no paper title or marker.
- Start the local development server and confirm `whitepaper.html` returns HTTP `200`.
- If remote authenticated preview is enabled, verify that an unauthenticated `GET` is rejected before content delivery and an authorized `GET` returns `200`. Verify private caching and robot-control headers where supported.
- Test `site-gate.js` separately as launch-screen behavior with mocked local and non-local locations. Do not count that test as publication-security evidence.
- Run cross-page negative assertions for inaccurate Panasonic attribution, broad patent claims, medical-purpose language, vulnerable-population benefits, `Breathing Sense`, `Zero Outages`, and other prohibited categorical claims.
- Verify that the privacy notice accurately scopes website versus product or app data and describes the contact handoff.
- Run `node --check script.js` if shared JavaScript changes are made.
- Run `git diff --check` and the existing site tests.
- Review final copy for unsupported medical, legal, patent, privacy, security, accuracy, compatibility, reliability, coverage, setup-time, and performance claims.

## Public-release gate

Public release requires all of the following:

- The production access model is intentionally changed from exclusion to publication and approved by the project owner.
- Document control, authorship, the linked revision-history section, citations, claim register, evidence cutoff, and applicable prototype revisions are complete.
- Every substantive empirical claim has an evidence status and required evidence or reference record, and every controlled disclosure has its required approval basis.
- One exact Panasonic entity and award-category string plus the Cantata-Haptique identity relationship are documented and approved, or the recognition is omitted.
- Patent filing status and wording are verified and approved, or the patent statement is omitted.
- The linked-site consistency audit passes.
- Product and companion-app privacy boundaries are documented before any human testing involving presence or Bluetooth proximity.
- Safety and failure-mode design targets are identified, and any implemented claims are supported by repeatable evidence.
- Accessibility, responsive behavior, content contracts, and publication-boundary tests pass.
- The final DOCX and PDF render audits pass, the artifacts agree on content and revision metadata, and both files are scanned to confirm that no unapproved personal metadata or comments remain.

## Future publication path

Revision metadata, authorship, citations, evidence status, and test conditions are required in the developer preview. A future public revision may expose the canonical PDF through an approved download route and add measured results, expanded datasets, and production specifications while preserving revision history and the prototype-versus-production distinction. The DOCX remains an internal editorial source unless separately approved for distribution.
