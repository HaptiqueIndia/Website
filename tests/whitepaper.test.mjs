import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const page = await readFile(new URL('../whitepaper.html', import.meta.url), 'utf8');
const style = await readFile(new URL('../style.css', import.meta.url), 'utf8');

assert.match(page, /<title>ROOT[^<]*Technical concept paper/i);
assert.match(
  page,
  /<meta name="robots" content="noindex,nofollow,noarchive,nosnippet">/i,
);
assert.equal((page.match(/<h1\b/gi) ?? []).length, 1, 'paper should have one h1');
assert.match(page, /<body class="ac-whitepaper-page" id="top">/i);
assert.doesNotMatch(page, /<body[^>]+class="[^"]*ac-product-page/i);
assert.match(page, />Companion web edition \/ D0\.1</i);
assert.doesNotMatch(page, /href\s*=\s*["'][^"']*\.(?:pdf|docx)(?:[?#][^"']*)?["']/i);
assert.match(page, /ROOT-TCP-001/i);
assert.match(page, /D0\.1/i);
assert.match(page, /25 August 2026/i);

const sectionIds = [
  'abstract',
  'room-level-problem',
  'architecture',
  'connectivity',
  'sensing',
  'placement',
  'evaluation',
  'limitations',
  'company',
  'references',
  'revision-history',
];

let previousSectionIndex = -1;
for (const id of sectionIds) {
  const marker = `id="${id}"`;
  const sectionIndex = page.indexOf(marker);
  assert.notEqual(sectionIndex, -1, `paper should include ${marker}`);
  assert.ok(sectionIndex > previousSectionIndex, `${id} should be in document order`);
  previousSectionIndex = sectionIndex;
}

for (const label of [
  'Cited background',
  'Implemented prototype behavior',
  'Hypothesis / design target',
  'Planned evaluation',
]) {
  assert.match(page, new RegExp(label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'));
}

for (const field of [
  'Document ID',
  'Revision',
  'Publication status',
  'Technical reviewer',
  'Evidence cutoff',
  'Hardware revision',
  'Firmware revision',
]) {
  assert.match(page, new RegExp(field, 'i'));
}

for (const claimId of ['CB-01', 'HT-01', 'HT-02', 'PE-01', 'PE-07']) {
  assert.match(page, new RegExp(claimId));
}

assert.match(page, /Conceptual architecture, not a measured result/i);
assert.match(page, /not a medical device/i);
assert.match(page, /not a safety-critical/i);
assert.match(page, /original AC remote/i);
assert.match(page, /Haptique Electronics Pvt\. Ltd\./i);
assert.match(page, /mailto:info@get-root\.in/i);
assert.match(page, /<figure\b[\s\S]*<figcaption\b/i);
assert.match(page, /<img[^>]+alt="[^"]{12,}"/i);
assert.match(page, /https:\/\/doi\.org\//i);
assert.match(page, /https:\/\/www\.bluetooth\.com\//i);

assert.doesNotMatch(
  page,
  /Acceleration Award|affiliated with Panasonic|patent pending|±0\.1|zero outages|perfect coverage|universal compatibility|breathing sense/i,
);
assert.doesNotMatch(page, /<script[^>]+site-gate\.js/i);
assert.doesNotMatch(page, /—/);

for (const selector of [
  '.ac-whitepaper-page',
  '.ac-whitepaper-hero',
  '.ac-whitepaper-document-grid',
  '.ac-whitepaper-architecture',
  '.ac-whitepaper-evaluation',
  '.ac-whitepaper-status',
]) {
  assert.match(style, new RegExp(selector.replace('.', '\\.')));
}

assert.match(
  style,
  /\.ac-whitepaper-page \.ac-whitepaper-section__body > p[^}]*max-width:\s*70ch/i,
);
assert.match(style, /\.ac-whitepaper-page[^}]*:focus-visible/i);
assert.match(style, /\.ac-whitepaper-page section[^}]*scroll-margin-top:\s*72px/i);
assert.match(
  style,
  /@media\s*\(max-width:\s*760px\)[\s\S]*\.ac-whitepaper-page section[^}]*scroll-margin-top:\s*68px[\s\S]*\.ac-whitepaper-document-grid[\s\S]*\.ac-whitepaper-architecture[\s\S]*\.ac-whitepaper-evaluation/i,
);

console.log('whitepaper contract: ok');
