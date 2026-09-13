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
