import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const repositoryRoot = dirname(dirname(fileURLToPath(import.meta.url)));

test('product page places only the requested responsive YouTube video before the hero', async () => {
  const html = await readFile(join(repositoryRoot, 'product-details.html'), 'utf8');
  const mainStart = html.indexOf('<main>');
  const videoStart = html.indexOf('class="ac-product-video"');
  const heroStart = html.indexOf('id="product-hero"');
  const videoMarkup = html.slice(videoStart, heroStart);

  assert.ok(videoStart > mainStart, 'video should be inside main');
  assert.ok(videoStart < heroStart, 'video should be the first section in main');
  assert.doesNotMatch(videoMarkup, /<(?:h[1-6]|p)\b/);
  assert.match(videoMarkup, /src="https:\/\/www\.youtube-nocookie\.com\/embed\/aNUCqgTFvj8"/);
  assert.match(videoMarkup, /title="ROOT product video on YouTube"/);
  assert.match(videoMarkup, /loading="lazy"/);
  assert.match(videoMarkup, /referrerpolicy="strict-origin-when-cross-origin"/);
  assert.match(videoMarkup, /allowfullscreen/);
  assert.match(videoMarkup, /style="[^"]*width:\s*100%[^"]*aspect-ratio:\s*16\s*\/\s*9[^"]*"/);
});
