import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { access, readdir, readFile } from 'node:fs/promises';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const repositoryRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const distRoot = join(repositoryRoot, 'dist');

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch {
    return false;
  }
}

async function collectText(path) {
  const entries = await readdir(path, { withFileTypes: true });
  const chunks = [];

  for (const entry of entries) {
    const entryPath = join(path, entry.name);
    if (entry.isDirectory()) {
      chunks.push(await collectText(entryPath));
      continue;
    }

    if (/\.(?:css|html|js|json|map|md|txt)$/i.test(entry.name)) {
      chunks.push(await readFile(entryPath, 'utf8'));
    }
  }

  return chunks.join('\n');
}

async function collectFiles(path) {
  const entries = await readdir(path, { withFileTypes: true });
  const files = [];

  for (const entry of entries) {
    const entryPath = join(path, entry.name);
    if (entry.isDirectory()) {
      files.push(...await collectFiles(entryPath));
    } else {
      files.push(relative(distRoot, entryPath));
    }
  }

  return files.sort();
}

test('current committed head carries the production builder and companion CSS contract', {
  skip: !(await exists(join(repositoryRoot, '.git'))),
}, () => {
  const committedBuilder = spawnSync('git', ['show', 'HEAD:scripts/build-production.mjs'], {
    cwd: repositoryRoot,
    encoding: 'utf8',
  });
  assert.equal(committedBuilder.status, 0, committedBuilder.stderr || committedBuilder.stdout);
  assert.match(committedBuilder.stdout, /production artifact: dist\//);

  const committedStyle = spawnSync('git', ['show', 'HEAD:style.css'], {
    cwd: repositoryRoot,
    encoding: 'utf8',
  });
  assert.equal(committedStyle.status, 0, committedStyle.stderr || committedStyle.stdout);
  assert.match(committedStyle.stdout, /\/\* ROOT technical concept paper \*\/[\s\S]*\.ac-whitepaper-page/);
});

test('production artifact excludes the local-only concept paper', async () => {
  const build = spawnSync(process.execPath, ['scripts/build-production.mjs'], {
    cwd: repositoryRoot,
    encoding: 'utf8',
  });

  assert.equal(build.status, 0, build.stderr || build.stdout);
  assert.equal(await exists(join(distRoot, 'index.html')), true);

  for (const excludedPath of [
    'whitepaper.html',
    'docs',
    'tests',
    'scripts',
    'Brand Story.docx',
    'Codex Image 24 Aug 2026, 22_21_31.png',
  ]) {
    assert.equal(
      await exists(join(distRoot, excludedPath)),
      false,
      `${excludedPath} must not exist in dist`,
    );
  }

  const outputText = await collectText(distRoot);
  assert.doesNotMatch(outputText, /whitepaper\.html/i);
  assert.doesNotMatch(outputText, /ROOT technical concept paper/i);
  assert.doesNotMatch(outputText, /ac-whitepaper-/i);
  assert.doesNotMatch(outputText, /A local architecture for room-level AC comfort/i);
  assert.doesNotMatch(outputText, /ROOT-Technical-Concept-Paper-D0\.1\.(?:pdf|docx)/i);
  assert.doesNotMatch(outputText, /ROOT-TCP-001/i);
  assert.doesNotMatch(outputText, /Companion web edition/i);
  assert.equal(await exists(join(distRoot, 'output')), false);

  assert.deepEqual(await collectFiles(distRoot), [
    'about.html',
    'assets/acboss-sleep-slide1-freezing.jpg',
    'assets/acboss-sleep-slide2-sweating.jpg',
    'assets/acboss-sleep-slide3-autopilot.jpg',
    'assets/renders/root-audience-arthritis.png',
    'assets/renders/root-audience-elders.png',
    'assets/renders/root-audience-kids.png',
    'assets/renders/root-matte-product-angle.png',
    'assets/renders/root-matte-wall-mount-plants.png',
    'assets/root-favicon.svg',
    'assets/root-matte-night-hero-v1.png',
    'assets/root-matte-product-handoff-editorial.png',
    'assets/root-matte-product-pebble-vector.jpg',
    'assets/root-matte-technical-cutaway-v1.png',
    'coming-soon.html',
    'index.html',
    'privacy-policy.html',
    'product-details.html',
    'script.js',
    'site-gate.js',
    'sitemap.html',
    'style.css',
  ]);
});
