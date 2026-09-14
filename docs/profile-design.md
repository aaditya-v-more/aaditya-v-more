# Profile artwork

The README uses original SVG illustrations, bold type and a restrained lime, cyan, coral and lilac palette. Each large image has a desktop and phone composition in both light and dark colors. GitHub selects them with `picture` sources.

## Update the artwork

Edit `scripts/generate-profile.py`, then regenerate the committed assets:

```sh
python3 scripts/generate-profile.py
```

The generator uses only the Python standard library. SVGs contain no remote assets, fonts or scripts. CSS animation is decorative and stops for visitors who prefer reduced motion. The default static drawing remains complete.

These are conceptual drawings, not product screenshots or live metrics. Keep README project claims grounded in the public repositories, preserve coauthor credits and textbook attribution, and keep real text and links outside the artwork for accessibility.

Before publication, inspect the rendered README on GitHub at desktop and phone widths, including its image sources, native text, links and wrapping. Review both color palettes. Keep each phone composition readable instead of shrinking a desktop panel. Commit and push reviewed updates to main.

## Keep media small and sharp

The generator automatically runs `scripts/optimize_svg.py`. It shortens numeric
notation and line paths without rounding coordinates, simplifying geometry,
changing colors, or removing animation. Keep the SVG format for crisp artwork
at any zoom level, along with all desktop, mobile, light and dark variants.

The September 2026 optimization reduced the 35 images from 485,590 to 381,950
bytes (21.3%). All 70 static comparisons at 1x and 2x resolution were pixel-identical.
An XML and exact-coordinate comparison also verified the animation styles,
paths, dimensions, accessibility attributes and element order. Gzip sizes vary
with the serving platform; these figures describe the committed files.

When changing the optimizer, compare rendered before/after images and verify
animation and reduced-motion behavior. Running the generator again should
produce identical files. Do not trade visible quality for smaller files.
Use periods, commas, colons or ordinary hyphens instead of em dashes in profile
copy, artwork titles, documentation and commit messages.
