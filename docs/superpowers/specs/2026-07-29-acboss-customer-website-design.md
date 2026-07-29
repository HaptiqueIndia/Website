# Acboss customer website design

## Goal

Create a single-page, customer-first website for Acboss, an offline edge-AI climate controller that upgrades an existing AC into a more comfortable, energy-aware cooling system. Visitors first discover Acboss as a thermostat, then learn how its bioclimatic autonomous Split AC control can reduce electricity use.

The site must make Acboss feel like an easy everyday upgrade rather than an investor presentation or a complicated smart-home platform.

## Audience and conversion

Primary audience: Indian households, especially first-time or price-conscious AC owners in tier-2 and tier-3 cities.

Important action: **Pre-order Acboss**, earned only after the visitor understands the problem, sees the evidence, and understands the product. A compact Pre-order link remains available in the navigation and the final section, but it is not the hero’s primary call to action. The initial interaction gathers customer intent; a future checkout or CRM endpoint can replace it without changing the page structure.

## Messaging

Hero headline: **Your AC, finally on autopilot.**

Hero supporting copy: **More comfort. Less energy. Zero manual fiddling.**

The page uses simple customer language, then substantiates the promise through Acboss’s local, sensor-driven control and real prototype evidence. It avoids unqualified superlatives and treats savings figures as indicative, with an actual-savings disclaimer.

The emotional idea is: **cold is not always comfortable**. Acboss exists to reduce the everyday frustration of manual AC operation and overcooling, especially overnight.

## Visual direction

Direction: **Everyday comfort, proved personally**.

The visual system feels bright, calm, and premium. A warm off-white foundation represents home; midnight blue creates technical confidence; electric blue signals cool air and active intelligence; a restrained warm yellow highlights savings and actions. Typography is oversized and editorial in the hero, then compact and highly legible in supporting copy.

The product is represented as a precise physical device surrounded by soft environmental gradients and ambient airflow rather than generic dashboard cards. The founder story begins in a quiet, over-cooled morning room; the mood then shifts from muted dry blue to balanced, comfortable light as Acboss takes over. The reference site’s narrative economy and large proof moments inform the pacing, but Acboss has an independent identity, copy, and composition.

## Page structure

1. **Navigation** — Acboss mark, anchored links for How it works, Savings, and FAQ, plus a high-visibility Pre-order button.
2. **Hero** — The headline and supporting copy, a product-led visual, and a small live-status treatment showing Auto Comfort mode. The primary action is “See why Acboss exists,” leading into the founder story; the secondary action is “Watch it work,” leading to the demo.
3. **Founder story** — A concise, personal origin: the founder’s experience waking in an over-cooled, dry room and dealing with sinus discomfort, followed by the decision to build a better way to cool. This is framed as personal experience, not a medical claim. The lead line is: **“Cold is not always comfortable.”**
4. **Proof in action** — The real Split AC demo video, presented before claims-heavy content. Supporting copy states that Acboss prototypes have been tested and refined over five months.
5. **Trust strip** — Clear customer benefits: works with existing ACs, no Wi-Fi required, and optimizes AC plus fan.
6. **Problem / payoff** — Relatable manual cooling habits contrasted with an automatic, stable comfort outcome.
7. **Meet Acboss** — Plain-language explanation of the device’s local sensor intelligence, precision IR control, and BLE setup.
8. **Why Acboss** — A decisive comparison that positions Acboss as an intelligent edge-AI climate system, not another way to send commands to an AC. It compares Acboss with an AC remote, a conventional IR controller, and a smart AC app across the customer-facing dealbreakers below.
9. **Savings evidence** — An understandable before/after comparison based on actual electricity-bill usage, with account numbers, addresses, and other personal details removed. This follows the demo and states the test context and variance disclaimer.
10. **Inside the early build** — A confident, tactile hardware-reveal section explaining what an early pre-order unit contains and why each component matters to comfort automation. It is placed after the visitor understands the value, so technical detail reinforces confidence rather than obscuring the story.
11. **How it works** — Three steps: place it, pair it, let it work. Emphasizes that the system runs locally, including when internet is unavailable.
12. **Pre-order** — The final invitation, introduced only after the full story and evidence. It explains exactly what early customers receive: a handmade, 3D-printed early unit built from the working prototype platform. Price and shipping dates remain explicitly unavailable until commercial terms are confirmed.
13. **FAQ and footer** — Compatibility, privacy, setup, offline behavior, early-unit expectations, plus contact and legal destinations.

### Comparison content

| What matters at home | AC remote | Conventional IR controller | Smart AC app | Acboss edge-AI climate control |
| --- | --- | --- | --- | --- |
| Feels the room, not just the AC | No | No | No | **Yes — temperature and humidity aware** |
| Adjusts cooling by itself | No | Usually manual or scheduled | Usually manual or scheduled | **Yes — continuously optimizes comfort** |
| Coordinates AC and fan | No | No | Rarely | **Yes — optimized together** |
| Works when internet is down | Yes | Often | Usually no | **Yes — entirely local** |
| Learns the right cooling response | No | No | No | **Yes — edge logic built for Indian conditions** |

The visual treatment makes Acboss the clear, calm focal column rather than burying the evidence in a dense feature matrix. The section headline should state the difference plainly: **“Control is not intelligence.”** Its supporting line: **“Acboss senses your room, makes decisions locally, and keeps your cooling working together.”**

### Proof content and claim guardrails

- The supplied Split AC demo video is the first proof asset and must show the physical product working before the comparison and savings sections.
- A short, honest timeline states that prototypes were tested and iterated for five months. It must not imply an independent certification or a larger trial than actually occurred.
- Electricity-bill evidence is presented as a before/after use case, with a transparent period, household context, and all personal billing information redacted. No visually altered bill values are permitted.
- Savings claims retain the deck-supported “up to 24%” cap, say that results vary by home and use, and do not combine unrelated tests into a single claim.
- The founder’s sinus discomfort and concern about dry, over-cooled rooms are framed as a personal origin story. Acboss is described as a comfort product and must not be positioned as medical treatment, prevention, or diagnosis.

### Early-build hardware content

The early-unit section and final pre-order section communicate the product honestly. The customer receives a handmade early version with a 3D-printed enclosure and the following working-system components:

| Component | Customer value |
| --- | --- |
| ESP32-C5 controller | Provides the processing foundation and supports both 5 GHz and 2.4 GHz Wi-Fi capability. |
| Human-presence sensor | Allows the system to understand whether a person is in the room before making comfort decisions. |
| IR transmitter and receiver | Learns the AC remote during setup, then sends the commands needed to control the existing Split AC. |
| Sensirion temperature and humidity sensor | Supplies high-quality room-condition inputs that guide Acboss’s local comfort logic. Sensirion is a Swiss sensor company. |
| Matter-ready platform | Designed to support a future Matter path; it must be described as “Matter-ready” and not Matter-certified until certification has actually been achieved. |

The product reveal must use a “built in the open” tone: early customers are receiving a real, tested, evolving device—not a finished mass-manufactured appliance. The pre-order section clearly explains the 3D-printed finish and early-unit nature before any contact form. It does not imply final consumer certifications, production readiness, or guaranteed compatibility beyond the tested setup.

## Interaction and behavior

- All header and secondary links scroll to their matching sections.
- The hero CTAs scroll only to the founder-story and demo sections. The navigation Pre-order link and final pre-order CTA scroll to the pre-order section.
- The pre-order form checks required name, email, and city fields in the browser, provides clear inline errors, and switches to a thank-you state after a valid submission.
- The proof video has a descriptive title, poster frame, captions when available, and a direct playback fallback if embedded playback is unavailable.
- The early-build reveal uses progressive disclosure: customer benefit first, technical component detail second, and no technical acronyms without a plain-language explanation.
- Motion is limited to ambient airflow, gentle device/status movement, and section reveals. `prefers-reduced-motion` disables nonessential movement.
- Focus states, semantic labels, readable color contrast, and keyboard-accessible controls are required.

## Technical shape

The first release is a static responsive landing page. It has one route, no authentication, database, or live checkout. Components remain small and purpose-specific: navigation, hero, benefit strip, product explanation, savings comparison, setup steps, pre-order form, FAQ, and footer. Content is kept local so a later CMS or checkout integration is a bounded replacement.

## Failure and edge handling

- Missing form values retain entered values and show field-specific errors.
- A submitted form never claims that payment was taken; it confirms only that pre-order interest was received.
- Narrow screens stack visual and content blocks without horizontal overflow.
- External fonts and images have deliberate fallbacks so core copy remains usable.

## Verification

- Production build passes.
- Desktop and narrow mobile layouts have no clipped copy, overlapping controls, or horizontal overflow.
- CTA anchors, FAQ controls, and form validation work using keyboard and pointer input.
- Reduced-motion behavior and color contrast are checked manually.
- Customer-facing savings claims match the supplied pitch deck and retain the variance disclaimer.
- The founder story, demo-video context, and electricity-bill period accurately match the evidence supplied for the launch.
- Billing screenshots are inspected to ensure personal information is not exposed.
- The pre-order section accurately describes the handmade, 3D-printed early unit and does not claim Matter certification or unearned production certifications.

## Out of scope

- Payments, inventory, order management, user accounts, a product configurator, and live CRM submission.
- Separate investor, hospitality, or smart-home platform pages.
