import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

const [home, sitemap, about, privacy, comingSoon, siteGate, product] = await Promise.all([
  readFile(new URL('../index.html', import.meta.url), 'utf8'),
  readFile(new URL('../sitemap.html', import.meta.url), 'utf8'),
  readFile(new URL('../about.html', import.meta.url), 'utf8'),
  readFile(new URL('../privacy-policy.html', import.meta.url), 'utf8'),
  readFile(new URL('../coming-soon.html', import.meta.url), 'utf8'),
  readFile(new URL('../site-gate.js', import.meta.url), 'utf8'),
  readFile(new URL('../product-details.html', import.meta.url), 'utf8')
]);

const primaryNav = home.match(/<ul class="nav-links">([\s\S]*?)<\/ul>/)?.[1] ?? '';
assert.equal(/Talk to us/i.test(primaryNav), false, 'homepage primary nav should not contain Talk to us');
assert.match(home, /<footer[\s\S]*href="privacy-policy\.html"[^>]*>Privacy policy<\/a>/i, 'homepage footer should link to the privacy policy');
assert.match(home, /<footer[^>]+class="[^"]*ac-global-footer/i, 'homepage should have the full site footer');
assert.match(home, /Haptique Electronics Pvt\. Ltd\./i, 'homepage footer should identify the company');
assert.match(home, /Panasonic Ignition/i, 'homepage footer should show the affiliation');
assert.match(home, /Acceleration Award, 2025/i, 'homepage footer should show the award');
assert.match(home, /Discuss on Discord/i, 'homepage footer should show the Discord community link');
assert.doesNotMatch(home, /Email Heptic Electronics|Email Haptique Electronics/i, 'homepage footer should not show a direct email link');
assert.match(home, /href="privacy-policy\.html"[^>]*>Privacy policy<\/a>/i, 'homepage footer should link to the privacy policy');

for (const phrase of ['Haptique Electronics Pvt. Ltd.', 'Panasonic Ignition', 'Patent pending']) {
  assert.match(sitemap, new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'), `sitemap should mention ${phrase}`);
}
assert.match(about, /Acceleration Award at Panasonic Ignition, 2025/i, 'about page should mention the award');

assert.match(sitemap, /href="https:\/\/discord\.com"/i, 'sitemap should provide a Discord link');
assert.match(sitemap, /<form[^>]+id="sitemapContactForm"/i, 'sitemap should contain the contact form');
assert.match(sitemap, /name="name"[^>]+required/i, 'contact form should require a name');
assert.match(sitemap, /name="email"[^>]+type="email"[^>]+required/i, 'contact form should require a valid email');
assert.match(sitemap, /name="message"[^>]+required/i, 'contact form should require a message');
assert.match(sitemap, /mailto:info@get-root\.in/i, 'contact form should hand off to the ROOT email address');

for (const phrase of ['Haptique Electronics Pvt. Ltd.', 'Willis Desai', 'Pradip Makwana', 'Panasonic Ignition']) {
  assert.match(about, new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'), `about page should mention ${phrase}`);
}
assert.match(about, /id="mission"/i, 'about page should include the company mission section');
assert.match(privacy, /<title>[^<]*Privacy policy/i, 'privacy page should have a privacy policy title');
assert.match(privacy, /How we use information/i, 'privacy page should explain information use');
assert.match(privacy, /mailto:info@get-root\.in/i, 'privacy page should provide a privacy contact');
assert.match(comingSoon, /Coming soon/i, 'coming-soon page should show the launch state');
assert.match(comingSoon, /Indoor climate, rethought/i, 'coming-soon page should communicate the climate promise');
assert.doesNotMatch(comingSoon, /Discuss on Discord|Haptique Electronics Pvt\. Ltd\.|Panasonic Ignition/i, 'coming-soon page should remain a minimal public gate');
assert.match(siteGate, /localhost|127\.0\.0\.1/i, 'site gate should allow local developer review');
assert.match(siteGate, /coming-soon\.html/i, 'site gate should redirect public traffic to coming-soon');
for (const page of [home, sitemap, about, privacy]) {
  assert.match(page, /<script src="site-gate\.js"/i, 'public pages should load the site gate');
}
assert.doesNotMatch(product, /Ask about compatibility/i, 'product page should not show the compatibility CTA');
assert.doesNotMatch(product, /<a href="about\.html">About<\/a>/i, 'product page should not show the About link');
assert.doesNotMatch(product, /ac-product-hero__eyebrow[\s\S]*?>ROOT<\/p>/i, 'product hero should not show a redundant ROOT eyebrow');

console.log('sitemap contract: ok');
