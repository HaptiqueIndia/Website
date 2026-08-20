# ROOT Responsive Performance Hardening

## Purpose

Improve the ROOT website's responsiveness in two equal dimensions: reliable layout behavior across modern phones, tablets, and desktop browsers, and lower-cost loading and interaction behavior. Preserve the existing static HTML/CSS/JavaScript architecture and editorial product-page visual system.

## Scope

Use targeted hardening rather than a broad CSS rewrite or progressive-loading redesign. Modify only the two HTML pages, the shared stylesheet, and the shared script unless verification identifies a directly related issue. Avoid introducing a framework, build step, or unrelated visual redesign.

## Responsive Layout

- Keep the current desktop navigation and simplify it at narrow widths without allowing wordmark, navigation, or CTA collisions.
- Use the existing page-scoped layout system with `clamp()`, `minmax(0, 1fr)`, and `min-width: 0` where needed to prevent grid children and long labels from widening the viewport.
- Make hero, story, benefit, setup, architecture, simulator, comparison, and enquiry regions collapse intentionally at tablet and mobile widths.
- Add stable image aspect-ratio behavior and responsive object sizing so major image regions do not jump while assets load.
- Preserve horizontal scrolling only for genuinely tabular content, with contained pinout and comparison table scrollers.
- Preserve semantic order, keyboard access, visible focus states, and reduced-motion support.

## Loading And Interaction Performance

- Keep first-viewport hero/product imagery eager; mark below-the-fold imagery for lazy loading and asynchronous decoding.
- Add intrinsic dimensions or equivalent aspect-ratio rules to major images to reduce cumulative layout shift.
- Pause carousel autoplay when its section is off-screen, the document is hidden, or reduced motion is enabled. Keep manual controls available.
- Fix simulator canvas resize handling so repeated resizes reset the drawing transform, cap device-pixel-ratio work, and animate only while the simulator is visible.
- Restrict 3D tilt listeners to fine-pointer devices, avoiding pointer-heavy work on touch screens.
- Apply reduced-motion behavior consistently to carousel autoplay, canvas animation, and decorative transitions.

## Files And Boundaries

- `index.html`: responsive image loading metadata and any required stable media dimensions.
- `product-details.html`: responsive image loading metadata and any required stable media dimensions.
- `style.css`: targeted layout, overflow, image sizing, pointer, and reduced-motion rules; avoid a wholesale selector consolidation.
- `script.js`: visibility-aware carousel and simulator scheduling, safe canvas resizing, and fine-pointer tilt gating.

## Verification

- Check both pages at narrow phone, tablet, and desktop widths in modern Safari and Chrome.
- Confirm there is no accidental horizontal overflow outside intentional table scrollers.
- Verify image loading attributes, stable major media regions, keyboard focus, carousel controls, gallery controls, architecture selection, and simulator sliders.
- Verify reduced-motion behavior disables carousel autoplay and continuous animation while preserving usable controls.
- Run JavaScript syntax validation and `git diff --check`.
- Review the final diff for selector interactions between the legacy base CSS and the page-scoped ROOT rules.

## Success Criteria

The pages remain visually consistent with the current ROOT design, render without accidental viewport widening on supported modern devices, avoid unnecessary animation work when content is not visible or the user prefers reduced motion, and retain all existing interactive paths.
