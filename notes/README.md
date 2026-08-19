# Research notes — how to add and maintain an entry

This folder is a chronological archive of seminar presentations, paper reviews and
methodological notes. Because `.nojekyll` sits at the repository root, **there is no build
step: HTML committed here is served exactly as written.**

## Folder layout

```
notes/
├── index.html                      archive index, grouped by year
├── _TEMPLATE.html                  template for a new note — copy this
├── README.md                       this file
└── YYYY-MM-DD-slug/                one note = one folder
    ├── index.html
    └── images/                     figures and tables (optional)
```

`assets/notes.css` holds the styles for this section. Every rule for the document body is
scoped under `.note-body`, so it cannot collide with the site-wide `assets/style.css`.

## Adding a note in three steps

**1. Create the folder**

```
notes/2026-09-10-rum-nn-review/
```

The naming rule is `YYYY-MM-DD-short-english-slug`. Because the date leads, folders sort
chronologically on their own and the URL doubles as a permanent link.

**2. Copy the template and fill it in**

```
cp notes/_TEMPLATE.html notes/2026-09-10-rum-nn-review/index.html
```

Replace only the placeholders marked `[[ ]]`. If the note has figures, create an `images/`
folder alongside `index.html` and reference them relatively: `<img src="images/fig1.png">`.

**3. Add one line to the index**

Paste an `<li>` block at the top of the `<ul class="note-list">` in `notes/index.html` and
edit the title, date, summary and topic tags. When the year changes, add a new
`<h2 class="year-h">2027</h2>` heading.

Then `git add . && git commit && git push`. The change appears in a minute or two.

## Formatting available in the body

| Class | Purpose |
|---|---|
| `.paperbox` | Bibliographic details of the paper under discussion |
| `.assume` | The model's assumptions as a numbered list |
| `.exbox` | Worked examples and analogies (`<span class="tt">` for the sub-heading) |
| `.notebox` | Caveats and supplementary remarks |
| `ol.steps` | An argument in numbered steps, with circular badges |
| `.eq` | Equation block (MathJax; keep the original paper's equation numbers) |
| `table.cmp` | Comparison table |
| `figure` + `figcaption` | Figure with caption |
| `a.cite` | In-text citation superscript, linked to `id="ref-n"` in `ol.refs` |

## Writing conventions

- **Citation.** Every equation and every claim carries a source. In-text citations take the form
  `<a class="cite" href="#ref-1">[1]</a>` and link to `<li id="ref-1">` in the References list.
- **Verifying references.** Cite only works whose journal, volume, article number and DOI have
  been confirmed against publisher or index records. If it cannot be confirmed, do not cite it.
  Where a preprint must be cited, say so explicitly.
- **Colour.** The body uses black, grey and dark grey only. Figures taken from source papers keep
  their original colours.
- **Abbreviations.** Spell out at first use, in the original language together with the meaning;
  use the short form thereafter.
- **Attribution.** When a note records a seminar given by someone else, credit the presenter in
  the header, in the archive entry and in the closing paragraph.
- **Copyright.** When reproducing a figure or table from a paper, cite the source in the caption.
  Files you have no right to redistribute — original PDFs, for instance — are not committed; see
  `.gitignore`.

## Previewing locally

No build is required, so opening the file in a browser works. To check relative paths exactly,
serve the repository root:

```
python3 -m http.server 4000
# → http://localhost:4000/notes/
```
