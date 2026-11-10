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

`master` is what Vercel deploys, so a merge to `master` is a deploy.

1. Never work in the shared clone. Make your own worktree from `origin/master`:
   `git worktree add ../virtualpytest-website-<slug> -b <type>/<slug> origin/master`
2. Commit there and push your branch (`git push -u origin <type>/<slug>`). Do not push or merge to `master` locally; a guard in the VirtualPyTest agent tooling refuses it, and the repo has no integration lane.
3. Open a PR and merge it on GitHub with a merge commit, titled `merge: <slug> — <what changed>` like the existing history:
   `gh pr create --base master --head <branch>` then `gh pr merge <n> --merge --subject "merge: <slug> — ..."`
4. Wait for the Vercel deploy, then verify the live page or file (for example `curl -s https://virtualpytest.com/site.js | grep <marker>`).

Backend endpoints used by the site (e.g. the Ask AI widget) live in the `virtualpytest` repo and must be deployed before the site change that calls them.
