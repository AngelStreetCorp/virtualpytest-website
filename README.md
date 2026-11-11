# VirtualPyTest — website

Marketing site for [VirtualPyTest](https://github.com/AngelStreetCorp/virtualpytest), the open-source, AI-native device testing & monitoring platform.

Plain static HTML/CSS, no build step. Deployed on Vercel.

- `index.html` — the site
- `images/` — screenshots and logo, sourced from `virtualpytest/pitch-deck`

## Local preview

```
python3 -m http.server 8000
```

## Working on the site and landing changes

`master` is what Vercel deploys, so a merge to `master` is a deploy. Nobody merges by hand: not you, not a PR button, not the manager. The **integration lane** (mycodebox, repo key `website`) merges your branch into `master`, runs the tests below on the merged tree and pushes `master`. It has no deploy scope: Vercel deploys from `master` on its own.

1. Never work in the shared clone. Make your own worktree from `origin/master`:
   `git worktree add ../virtualpytest-website-<slug> -b <type>/<slug> origin/master`
2. Test in the worktree: `python3 -m pytest tests -q` (about 100 s; needs `python3-playwright` and its Chromium). It checks that the JSON files parse and that every Learn lesson fits a phone (`tools/learn_fit.py`, below).
3. Commit there and push **your branch only**: `git push -u origin <type>/<slug>`. A push to `master` is refused by the guard in the VirtualPyTest agent tooling, on purpose; the lane does the push to `master` from its own clone.
4. Ask the lane to integrate: `integrate request <type>/<slug> --repo website --wait` (no `--deploy`). It prints a request id; `integrate status <id>` shows where it is. Exit 0 = merged. Exit 3 = returned with a reason (fix it on your branch, push, request again). On a Mac the same command works with the Mac `integrate` client (token in `~/.config/mycodebox/token`, see mycodebox `docs/MAC-HOOK.md`); run it with `--wait` since nothing wakes a Mac session.
5. After the merge Vercel deploys `master`. Verify the live page or file (for example `curl -s https://virtualpytest.com/site.js | grep <marker>`). The lane removes your branch; remove the worktree: `git worktree remove ../virtualpytest-website-<slug>`.

The manager is only involved when the lane returns a request that needs a decision (paths such as `.github/workflows/*`, secrets); never open a PR to get around the lane.

Backend endpoints used by the site (e.g. the Ask AI widget) live in the `virtualpytest` repo and must be deployed before the site change that calls them.

## Folder pages need their trailing slash

`learn/` loads its cards, translations and script by relative path (`cards/<name>.html`, `i18n/`, `learn_i18n.js`). Opened as `/learn` without the slash, they resolve to the site root and the player shows Vercel's 404 ("This page doesn't exist"). The cards are not missing. Two guards stop this; keep both:

- `vercel.json` has `"trailingSlash": true`, so `/learn` answers with a 308 to `/learn/`.
- `learn/index.html` redirects to the slash form in its `<head>`, for any other host.

A new folder page (`<name>/index.html`) with relative paths needs the same `<head>` guard. After a deploy, check: `curl -sI https://virtualpytest.com/learn` returns 308 with `location: /learn/`.

## Learn phone-fit check

`python3 tools/learn_fit.py [site-dir] [height, default 740] [--lang de]` opens every Learn lesson at 390 px wide and requires that the lesson block (`main.lx`: picker, animation, text, sticky Prev/Next) is no taller than the viewport, that every title stays on one line and that no card throws a page error. The site navbar, device strip and footer scroll away and are not counted. It exits 1 on any failure and is part of `python3 -m pytest tests -q`, which the lane runs. (Before 2026-11-11 the check counted the whole page, so all 50 lessons "failed" by a constant 400 px. The lessons themselves were fine.)

## Editing the pages

`index.html`, `site.css`, `site.js` and `locales.json` are the source: edit them directly, through the lane as above. Do not regenerate them from any script.

A local-only `mockups/` folder (design mockups and a `port_site.py` generator) may exist on some machines. It is gitignored on purpose, is not part of this repository, and must never be committed or pushed. It has fallen behind `master`, so running its generator would overwrite current pages.
