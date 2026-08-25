import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { access, readdir, readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
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
});
