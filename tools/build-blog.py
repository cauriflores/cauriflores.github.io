#!/usr/bin/env python3
"""Generate the writing section from the sources in src/.

The site is served with .nojekyll, so GitHub Pages copies files rather than
building them. That is deliberate: /privacy.html and the Pacheco support page
are in the App Store Connect listing, and a build that can fail is a build that
can take them down. Pages here are generated on this machine and committed, the
same way the Angular app is.

    python3 tools/build-blog.py

Each post is a directory under src/posts/<slug>/ holding:

    post.json   { "date": "2026-09-05",
                  "title": {"en": ..., "es": ...},
                  "summary": {"en": ..., "es": ...} }
    en.html     the body, as HTML fragments — no <html>, no <body>
    es.html     the same in Spanish

Both languages ship in every page and stack without JavaScript, which is how
the rest of this site already works: nobody is left without something readable.
"""

import html
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "posts"
POSTS_OUT = ROOT / "posts"
WRITING_OUT = ROOT / "writing"

ASSET_VERSION = 4  # bump when style.css or lang.js changes, or browsers cache the old one

NAV = [
    ("writing", "/writing/", "Writing", "Escritos"),
    ("pacheco", "/pacheco/", "Pacheco", "Pacheco"),
    ("support", "/support/", "Support", "Soporte"),
    ("privacy", "/privacy.html", "Privacy", "Privacidad"),
]

MONTHS = {
    "en": "January February March April May June July August September October November December".split(),
    "es": "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split(),
}


def long_date(iso: str, lang: str) -> str:
    y, m, d = (int(part) for part in iso.split("-"))
    month = MONTHS[lang][m - 1]
    return f"{month} {d}, {y}" if lang == "en" else f"{d} de {month} de {y}"


def nav_html(current: str, lang: str, depth: int) -> str:
    links = []
    for key, href, en, es in NAV:
        label = en if lang == "en" else es
        if key == current:
            links.append(f'<a href="{href}" aria-current="page">{label}</a>')
        else:
            links.append(f'<a href="{href}">{label}</a>')
    return "<nav>" + "".join(links) + "</nav>"


def page(*, title_en, title_es, description, body_en, body_es, current, depth) -> str:
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title_en)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{up}favicon.ico?v={ASSET_VERSION}" sizes="any">
<link rel="icon" type="image/png" href="{up}favicon-32.png?v={ASSET_VERSION}" sizes="32x32">
<link rel="apple-touch-icon" href="{up}apple-touch-icon.png?v={ASSET_VERSION}">
<meta name="theme-color" content="#c2185b">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<link rel="stylesheet" href="{up}style.css?v={ASSET_VERSION}">
</head>
<body>
<div class="wrap">

  <div class="langbar" hidden>
    <button type="button" data-lang="en">English</button>
    <button type="button" data-lang="es">Español</button>
  </div>
  <span hidden data-title-en="{html.escape(title_en)}" data-title-es="{html.escape(title_es)}"></span>

  <div class="langblock" lang="en">
{body_en}
  </div>

  <div class="langblock" lang="es">
{body_es}
  </div>

</div>
<script src="{up}lang.js?v={ASSET_VERSION}"></script>
</body>
</html>
"""


def post_body(meta, body, lang, current="writing") -> str:
    title = meta["title"][lang]
    back = "All writing" if lang == "en" else "Todos los escritos"
    return f"""  <header>
    <p class="eyebrow">{long_date(meta['date'], lang)}</p>
    <h1>{html.escape(title)}</h1>
    <p class="lede">{html.escape(meta['summary'][lang])}</p>
    {nav_html(current, lang, 2)}
  </header>

{body.rstrip()}

  <footer>
    <p><a href="/writing/">&larr; {back}</a></p>
  </footer>"""


def index_body(posts, lang) -> str:
    heading = "Writing" if lang == "en" else "Escritos"
    lede = (
        "Notes on the things I build, and how they turned out."
        if lang == "en"
        else "Notas sobre lo que construyo, y cómo resultó."
    )
    empty = "Nothing here yet." if lang == "en" else "Todavía no hay nada."

    items = []
    for meta, slug in posts:
        items.append(
            f"""    <article class="entry">
      <p class="entry-date">{long_date(meta['date'], lang)}</p>
      <h2><a href="/posts/{slug}/">{html.escape(meta['title'][lang])}</a></h2>
      <p>{html.escape(meta['summary'][lang])}</p>
    </article>"""
        )

    listing = "\n".join(items) if items else f"    <p>{empty}</p>"
    return f"""  <header>
    <p class="eyebrow">Cauri Flores</p>
    <h1>{heading}</h1>
    <p class="lede">{lede}</p>
    {nav_html('writing', lang, 1)}
  </header>

{listing}"""


def main() -> int:
    posts = []
    if SRC.exists():
        for directory in sorted(SRC.iterdir()):
            if not (directory / "post.json").exists():
                continue
            meta = json.loads((directory / "post.json").read_text())
            for field in ("date", "title", "summary"):
                if field not in meta:
                    sys.exit(f"{directory.name}: post.json is missing {field!r}")
            for lang in ("en", "es"):
                if not (directory / f"{lang}.html").exists():
                    sys.exit(f"{directory.name}: missing {lang}.html — both languages ship")
            posts.append((meta, directory.name))

    # Newest first, and a date that has not happened yet is almost always a typo.
    posts.sort(key=lambda item: item[0]["date"], reverse=True)
    today = date.today().isoformat()
    for meta, slug in posts:
        if meta["date"] > today:
            print(f"  note: {slug} is dated {meta['date']}, which is in the future")

    for meta, slug in posts:
        directory = SRC / slug
        out = POSTS_OUT / slug
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(
            page(
                title_en=meta["title"]["en"],
                title_es=meta["title"]["es"],
                description=meta["summary"]["en"],
                body_en=post_body(meta, (directory / "en.html").read_text(), "en"),
                body_es=post_body(meta, (directory / "es.html").read_text(), "es"),
                current="writing",
                depth=2,
            )
        )
        print(f"  /posts/{slug}/")

    WRITING_OUT.mkdir(parents=True, exist_ok=True)
    (WRITING_OUT / "index.html").write_text(
        page(
            title_en="Writing — Cauri Flores",
            title_es="Escritos — Cauri Flores",
            description="Notes on the things I build, and how they turned out.",
            body_en=index_body(posts, "en"),
            body_es=index_body(posts, "es"),
            current="writing",
            depth=1,
        )
    )
    print(f"  /writing/  ({len(posts)} post{'s' if len(posts) != 1 else ''})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
