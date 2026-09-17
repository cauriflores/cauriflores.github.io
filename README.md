# cauriflores.github.io

Support and privacy pages for **Pacheco**, a weather app for iPhone.

- Support — https://cauriflores.github.io/
- Privacy policy — https://cauriflores.github.io/privacy.html

Plain HTML and CSS, no build step. The contact address is stored as two base64
halves and assembled in the browser by `mail.js`, so the literal string never
appears in the served source.

## ⚠️ This repo is frozen on purpose

**Both URLs above are in the App Store Connect listing**, and Apple checks the
privacy one. The Support URL is a *version-level* field there: changing it
requires a new app version and a full App Review, whatever else is in the
submission. So these two files do not move, and nothing else gets built here.

Everything else — the writing, the Pacheco web app, whatever comes next —
lives at **https://cauriflores.com/** (repo `cauriflores/web`), on its own
domain so that publishing can never reach the pages Apple has on file. Until
2026-09-17 this repo also held `/writing/`, `/posts/` and `/pacheco/`, and the
Angular deploy rsynced `--delete` straight into it; both are gone.

`/support/` is the same support page at a second URL, linked from the nav on
cauriflores.com. Its links to the writing and the app are absolute, because
they are on the other host now.

## The freeze is enforced

`.githooks/pre-commit` refuses any commit that stages `index.html` or
`privacy.html`, and explains why. It is wired up with:

```bash
git config core.hooksPath .githooks
```

**That config is local and does not survive a fresh clone** — `.githooks/` is
versioned, but the setting is not. Re-run the line above after cloning, or the
hook is silently inactive.

To edit those two files deliberately, having accepted that it costs a new app
version and a full App Review: `git commit --no-verify`.

Everything else in this repo commits normally. The hook guards two files, not
the repo.
