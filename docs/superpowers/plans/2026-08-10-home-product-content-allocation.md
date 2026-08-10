# ACBOSS Home/Product Content Allocation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate ACBOSS discovery content from detailed product-evaluation content without losing existing homepage work.

**Architecture:** `index.html` retains only the emotional discovery narrative and a clear product handoff. `product-details.html` becomes the canonical detail page by receiving the relocated sections. `script.js` continues to initialize controls only when their associated markup is present.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript.

## Global Constraints

- Use `ACBOSS` for public-facing branding.
- Move content, do not duplicate it.
- Do not claim a confirmed reservation or transaction.

---

### Task 1: Reduce the homepage to discovery content

**Files:**
- Modify: `index.html`

- [ ] Retain the hero, three-benefit introduction, comfort thesis, and sleep-story carousel.
- [ ] Replace detailed product evaluation sections with a single image-led product handoff and CTA to `product-details.html`.
- [ ] Retain no duplicate setup, mounting, hardware, simulator, comparison, enquiry form, or full FAQ markup.
- [ ] Verify each retained navigation target exists and `git diff --check` reports no whitespace errors.

### Task 2: Make product details the complete evaluation path

**Files:**
- Modify: `product-details.html`, `style.css`, `script.js`

- [ ] Insert the relocated detailed problem, setup, mounting, hardware, simulator, comparison, FAQ, and email enquiry sections after the existing product narrative.
- [ ] Keep the existing product gallery and make each moved interaction target available on the product page.
- [ ] Apply product-page-scoped layout rules for the moved sections and mobile table behavior.
- [ ] Verify JavaScript syntax, internal anchors, and `git diff --check`.
