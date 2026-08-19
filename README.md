# phantomdotexe

A self-contained comic reader. One HTML file per work — no build step, no bundler,
no framework. Open a file and it runs.

**Reader features:** paged and continuous-scroll modes, chapter menu, bookmarks,
adjustable reading width, auto-advance, thumbnail grid, fullscreen, keyboard
shortcuts, and zoom with drag-to-pan and pinch support.

**Page images are not stored here.** Each reader points at its own image host and
loads panels one at a time, so pages open immediately rather than downloading an
archive first.

**Dependencies:** one — [Panzoom](https://github.com/timmywil/panzoom) (MIT),
vendored in `vendor/`. Nothing else, and nothing loaded from a CDN.

**Layout**

| Path | What |
|---|---|
| `index.html` | Landing page, listing every work |
| `*.html` | One reader per work, config at the top of the first `<script>` |
| `reader-template.html` | The blank template new readers are built from |
| `tools/` | Scripts that apply reader changes across every built page |
| `vendor/` | Panzoom |

Art by Snadiya.
