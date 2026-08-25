import { access, copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const repositoryRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const outputRoot = join(repositoryRoot, 'dist');

const publicFiles = [
  'index.html',
  'product-details.html',
  'about.html',
  'sitemap.html',
  'privacy-policy.html',
  'coming-soon.html',
  'script.js',
  'site-gate.js',
];

const publicAssets = [
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
];

for (const relativePath of [...publicFiles, 'style.css', ...publicAssets]) {
  try {
    await access(join(repositoryRoot, relativePath));
  } catch {
    throw new Error(`Missing production input: ${relativePath}`);
  }
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });

for (const relativePath of publicFiles) {
  await copyFile(join(repositoryRoot, relativePath), join(outputRoot, relativePath));
}

for (const relativePath of publicAssets) {
  const destination = join(outputRoot, relativePath);
  await mkdir(dirname(destination), { recursive: true });
  await copyFile(join(repositoryRoot, relativePath), destination);
}

const localOnlyStylesMarker = '/* ROOT technical concept paper */';
const sourceStyles = await readFile(join(repositoryRoot, 'style.css'), 'utf8');
const localOnlyStylesStart = sourceStyles.indexOf(localOnlyStylesMarker);

if (localOnlyStylesStart === -1) {
  throw new Error('Missing local-only concept paper styles marker');
}

await writeFile(
  join(outputRoot, 'style.css'),
  `${sourceStyles.slice(0, localOnlyStylesStart).trimEnd()}\n`,
  'utf8',
);

console.log('production artifact: dist/');
