import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const repositoryRoot = dirname(dirname(fileURLToPath(import.meta.url)));

test('product page adds only the requested responsive YouTube video after the hero', async () => {
  const html = await readFile(join(repositoryRoot, 'product-details.html'), 'utf8');
  const heroEnd = html.indexOf('</section>', html.indexOf('id="product-hero"'));
  const benefitsStart = html.indexOf('id="benefits"');
  const betweenHeroAndBenefits = html.slice(heroEnd, benefitsStart);

  assert.match(betweenHeroAndBenefits, /class="ac-product-video"/);
  assert.doesNotMatch(betweenHeroAndBenefits, /<(?:h[1-6]|p)\b/);
  assert.match(betweenHeroAndBenefits, /src="https:\/\/www\.youtube-nocookie\.com\/embed\/aNUCqgTFvj8"/);
  assert.match(betweenHeroAndBenefits, /title="ROOT product video on YouTube"/);
  assert.match(betweenHeroAndBenefits, /loading="lazy"/);
  assert.match(betweenHeroAndBenefits, /referrerpolicy="strict-origin-when-cross-origin"/);
  assert.match(betweenHeroAndBenefits, /allowfullscreen/);
  assert.match(betweenHeroAndBenefits, /style="[^"]*width:\s*100%[^"]*aspect-ratio:\s*16\s*\/\s*9[^"]*"/);
});
