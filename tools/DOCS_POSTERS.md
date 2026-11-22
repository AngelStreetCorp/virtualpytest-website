# Docs posters: one concept, one image

The Docs page (`/docs/`) is a series of big vertical posters. Each poster explains one concept or the architecture in a
single image. First poster: "What is VirtualPyTest?" (`docs/img/what-is-virtualpytest.svg`).

## Files

| What | Where |
|---|---|
| Poster image (SVG, 1200 wide, as tall as needed) | `docs/img/<id>.svg` |
| Generator, also the template to copy | `tools/make_docs_poster_what_is.py` |
| Series page (tabs, thumbnail) | `docs/index.html`, list `POSTERS` |
| Full-page viewer (centered, back, share X / LinkedIn / WhatsApp, download) | `docs/view/index.html`, object `P` |
| Home "How it works" thumbnail | `index.html`, `.how-poster` (links to `docs/view/#what-is`) |

`<id>` is a short kebab-case slug (`what-is`, `navigation-tree`). The viewer URL is `/docs/view/#<id>`.

## Anatomy of a poster (copy the template, change the text)

1. Eyebrow in gold caps, big title (a question or a noun phrase), one or two grey lines under it.
2. Six or fewer numbered layer panels, top to bottom, joined by a gold arrow. Each panel: gold number circle,
   bold title, one grey line, then 3 to 5 chips (bold name + grey caption), then one grey sentence.
3. Optional special panel (for example the small navigation graph in step 3) when a picture says more than chips.
4. A gold band at the bottom for the cross-cutting idea (in the first poster: the AI / MCP layer), then the footer line.

Canvas 1200 wide, panels x=60..1140, dark background `#161616` (looks right in both site themes, so the image
never changes with the theme). Palette: panel `#212121`, chip `#2a2a2a`, line `#3a3a3a`, text `#f2f2f2`, grey
`#a8a8a8`, gold `#e0a96d`. Font stack: Geist, then system fonts (an SVG in an `<img>` cannot load web fonts).

## Rules

- Plain, short words. Chip name at most about 16 characters, caption at most about 24. No em dashes.
- Every claim comes from the site (`index.html` features, the Learn lessons, the product docs). Do not invent features.
- Chip row maths, panel inner width is 1080: 4 chips of 240 with gap 18, or 5 chips of 190 with gap 17. Wider rows overflow.
- Escape `&` as `&amp;` in the text. The SVG must be well-formed XML:
  `python3 -c "import xml.dom.minidom as m;m.parse('docs/img/<id>.svg')"`.
- Reuse the words of the Learn lessons so the two series agree (for example "UI variables": one navigation tree,
  every build).

## Add a poster

1. Copy `tools/make_docs_poster_what_is.py` to `tools/make_docs_poster_<id>.py`, change the text and the output path,
   run it from the repo root.
2. Add an entry `{id, title, src, alt}` to `POSTERS` in `docs/index.html` and to `P` in `docs/view/index.html`
   (the viewer `src` is relative to `docs/view/`, so `../img/<id>.svg`).
3. Look at it: serve the repo (`python3 -m http.server`), open `/docs/` and `/docs/view/#<id>` at desktop and 900 px wide.
4. Ship: commit, push, `integrate request <branch>`, `integrate wait <id>`, then check the live
   `https://virtualpytest.com/docs/img/<id>.svg` returns 200 and send the owner the viewer link.

## Ideas for the next posters

Navigation tree, Localize and fingerprint, KPIs (loading time, zapping), hosts anywhere (architecture), incidents and
monitoring, AI and MCP. Each one as a vertical flow like the first.
