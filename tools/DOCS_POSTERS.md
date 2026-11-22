# Docs posters: one concept, one image

The Docs page (`/docs/`) is a series of big vertical posters. Each poster explains one concept or the architecture in a
single image. First poster: "What is VirtualPyTest?" (`docs/img/what-is-virtualpytest.svg`).

## Files

| What | Where |
|---|---|
| Poster image (SVG, 1200 wide, as tall as needed) | `docs/img/<id>.svg` |
| Generator, also the template to copy | `tools/make_docs_poster_what_is.py` |
| Series page (a dropdown that groups posters by Learn topic, "Watch the lesson" link) | `docs/index.html`, list `POSTERS` (`topic`, `learn`) |
| Full-page viewer (centered, back, share X / LinkedIn / WhatsApp, download) | `docs/view/index.html`, object `P` |
| Home "How it works" thumbnail | `index.html`, `.how-poster` (links to `docs/view/#what-is`) |
| Share image (PNG 1200x630, the top of the poster) and share page (Open Graph / Twitter card tags) | `docs/img/<id>-share.png`, `docs/view/<id>/index.html`, written by `tools/make_docs_share.py` |

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


## Stories, titles and the Learn link (owner 2026-11-22)

- A poster belongs to one **Learn topic** (`topic: '7 · AI in the lab'` in `POSTERS`): the dropdown groups posters under
  the Learn topic names. Use the **same title as the Learn lesson** (or its Go deeper) and no new words: the Freeze
  poster is "Freeze: menu or stuck video?", as in lesson 7.5 and its Go deeper.
- `learn:` is the Learn hash the "Watch the lesson" button opens (`'0.1'`, `'7.5/deep'`).
- The Docs page script is plain JS in single-quoted strings: **never put an apostrophe in `title` or `alt`** ("model's"
  broke the page on 2026-11-22). Check the page script parses and that `/docs/` shows no page error.

## A poster that explains a doc (owner 2026-11-22)

- **Same structure, same words as the doc.** One card per doc section, in the doc's order, with the doc's section
  title word for word, and chips named with the doc's item names (table rows). Invent no labels (no "jobs", no "rules",
  no "Screen memory" unless the doc says it there). Example: `ai-use-cases` mirrors `docs/ai/AI-USE-CASES.md`.
- **First card = the overview**: one chip per doc section (the doc's titles), before the detailed cards. A section that
  is not a use case (for example "What is NOT AI") is not a chip there; it gets its own detailed card, with no number.
- **No date on a poster**, ever ("checked on ...", "to 2026-11-22"). A period the doc states ("30 days", "7 days") is fine.
- **Chips must fit the fallback font.** Headless Chromium has no Geist / Inter and falls back to DejaVu Sans, which is
  wider. Label 22 px bold in a 190 px chip holds about 11 characters; use 2 or 3 chips per row for long names.
  `tools/make_docs_poster_ai.py` measures every label with DejaVu Sans (PIL) and fails when one is too wide: copy that.
- **Look at the render**: inline the SVG with Playwright `set_content` (an `<img src=file://...>` renders blank),
  viewport 1200 x full height, screenshot it in 3 slices and read each one.

## Examples in a poster (owner 2026-11-22; drawn since the manager rule: no brand, no third-party screenshot)

A "Real examples" step shows real screens with the real decision. Rules: neutral sources only (our own pages, a public
page, a free streaming app; never an operator or provider app), real OCR words (tesseract), the real model's score and
decision, small thumbnails (320x180 JPG in `docs/img/<id>-real-<name>.jpg`, embedded in the SVG as base64), say the
first and last frame are the same. The model itself never goes on the page, only its results. Run the model on the example before you write its caption: a screensaver has no words, so it scores 0.00 (video, alert kept), not menu.

## Share a poster (X, LinkedIn, WhatsApp)

Share the link **`https://virtualpytest.com/docs/view/<id>/`**, not `.../view/#<id>`: social crawlers ignore the `#`.
That page carries the Open Graph and Twitter card tags and a prepared **PNG** (X and LinkedIn do not show SVG). Nothing
is generated at share time: run `python3 tools/make_docs_share.py` after a poster changes and commit the PNG and
`docs/view/<id>/index.html`. A new poster also needs its row in `POSTERS` inside `tools/make_docs_share.py`.

## Add a poster

1. Copy `tools/make_docs_poster_what_is.py` to `tools/make_docs_poster_<id>.py`, change the text and the output path,
   run it from the repo root.
2. Add an entry `{id, title, topic, learn, src, alt}` to `POSTERS` in `docs/index.html` and to `P` in `docs/view/index.html`
   (the viewer `src` is relative to `docs/view/`, so `../img/<id>.svg`).
3. Run `python3 tools/make_docs_share.py` (share PNG and share page). Look at it: serve the repo (`python3 -m http.server`), open `/docs/` and `/docs/view/#<id>` at desktop and 900 px wide.
4. Ship: commit, push, `integrate request <branch>`, `integrate wait <id>`, then check the live
   `https://virtualpytest.com/docs/img/<id>.svg` returns 200 and send the owner the viewer link.

## Ideas for the next posters

Navigation tree, Localize and fingerprint, KPIs (loading time, zapping), hosts anywhere (architecture), incidents and
monitoring, AI and MCP. Each one as a vertical flow like the first.

Drawn examples (freeze poster): draw each screen in HTML with generic labels, screenshot it with headless Playwright, read it with tesseract, score the words with the real model (device label `lab`, the label is part of its input) and print the score it returns; never pick a number by hand. A screenshot of a provider, broadcaster or operator app is never used.
