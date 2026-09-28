This is a master thesis template for the students from the [Faculty of Engineering Technology](https://iiw.kuleuven.be/english). 


## Interesting Resources (ordered according to relevance/importance)

- [LaTeX Workshop](https://github.com/GillesC/LaTeX-Workshop/blob/main/LaTeX_Workshop.pdf)
- [Intro LaTeX](https://github.com/dramco-edu/LaTex)
- [Writing scientific documents in LaTeX](https://github.com/DRAMCO/writing-scientific-papers-in-latex-tips-and-tricks)

## Using the template

Change your campus, language and other information in `thesis.tex`.

```latex
% Information about your discipline
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\programme{programme name}
\specialisation{specialisation}
\campus{ghenteng} % Selects the English Ghent cover, language, and campus rules
\title{Master's thesis title}
\subtitle{Subtitle (optional)}
\forenameA{first name}
\surnameA{last name}
\forenameB{} %keep empty if no 2nd author
\surnameB{} %keep empty if no 2nd author
\academicyear{2023 - 2024}
```

The example chapters are `chapters/chapter1.tex`, `chapters/chapter2.tex`, and
`chapters/chapter3.tex`; the example appendix is `chapters/appendix1.tex`.
The optional symbol list is `chapters/symbols.tex` (enable `longtable` when using it).
Use `\supervisorA`, `\supervisorB`, and `\supervisorC` to set supervisor details.
The older metadata commands `\opleiding`, `\afdeling`, and `\promotorA`, `\promotorB`, and `\promotorC`
remain available for compatibility. Dutch campus identifiers and Dutch-language
cover and front-matter text are retained for Dutch theses.

### Campus layout and content-page limits

The `\campus{...}` setting also selects the rules in `campus-profiles.tex`.
Dutch and English variants share the same layout and limit:

| Campus | Dutch / English value | Content columns | Maximum content pages |
| --- | --- | --- | --- |
| Ghent | `gent` / `ghenteng` | 2 | 20 |
| De Nayer | `denayer` / `denayereng` | 1 | Not configured |
| Geel | `geel` / `geeleng` | 1 | Not configured |
| Group T | `groept` / `groupteng` | 1 | Not configured |
| Bruges | `brugge` / `brugeseng` | 1 | Not configured |

Ghent uses `layout=paper` for its content: 10-point serif text with 12-point
line spacing, 2 cm margins, a 9 mm column gap, and a full-width title, subtitle,
and author block. Chapters become compact numbered headings that flow through
the columns without starting a new page; existing `\chapter`, `\section`,
labels, and table-of-contents entries still work. Page numbers appear at the
bottom, and paragraphs and display equations use tighter spacing.

The extended-paper styling applies between `\thesiscontent` and
`\finishthesiscontent`; the surrounding material retains the report layout.
These typography choices are template defaults and can be adapted to your programme.
To retain the previous heading and margin style, use
`\campussetup{layout=report}`. Column count and page limit are separate settings.

The other campuses retain the previous layout until their rules are supplied.
Edit their entries in `campus-profiles.tex` to configure them. A limit of `0`
disables the warning. For a programme-specific exception, add an override in
`thesis.tex` after `\campus`:

```latex
\campussetup{layout=report,columns=1,max-content-pages=30}
```

`\thesiscontent` starts the selected column layout, resets Arabic numbering to
page 1, and starts counting pages. `\finishthesiscontent` flushes pending figures
and tables, checks the limit, and restores one column. The supplied document
places these commands around the chapters, excluding the covers, front matter,
acronym list, bibliography, appendices, article, poster, and code of conduct.
If your programme counts references as content, move `\finishthesiscontent` after
`\printbibliography`.

The compilation log reports the content-page count and warns when it exceeds
the configured maximum; content is never truncated. The count includes float-only
pages inside the marked content, and is independent of page-number resets.
If `\finishthesiscontent` is omitted, counting continues to the end of the document.

In two-column content, size ordinary figures and tables using `\linewidth`.
Use `figure*` or `table*` for material spanning both columns. Wide floats may
move to a later page, which is included in the content-page count.

### Options

#### NL
- denayer
- geel
- gent
- groept
- brugge

#### EN
- denayereng
- geeleng
- ghenteng
- groupteng
- brugeseng


## FAQ

### The cover/back of my campus need to be changed

**Update: please submit an issue and I'll resolve it. Currently, all campuses should be in there**

Renaming of campuses is unfrntualy not uncommon. For now, to update your cover and back, go to the [official KU Leuven template website](https://iiw.kuleuven.be/english/students/master-thesis/templates) and download the Word version of the template.
Remove all text except the header and footers and save it as a PDF (one page per cover/back). Add the new cover by cloning this repo, add the covers/back to your repo and create a PR back to this repo. 


## Compiling

From the project directory, run:

```sh
latexmk -pdf thesis.tex
```

For LuaLaTeX, use `latexmk -lualatex thesis.tex`. The project `latexmkrc`
enables shell escape for the `minted` examples; Pygments (`pygmentize`) must
be available on your PATH. Latexmk runs Biber and repeats LaTeX as needed.
The sources use UTF-8 with either engine.

## Checking campus rules

With Python 3 and `pdflatex` installed, run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

These checks compile minimal documents for all campus/language combinations,
column transitions, page limits, overrides, and pending floats. Build products
are kept in temporary directories.

## Bugs and extensions
If you find a bug or want to request an extension to the template, you have two options:
1. For the geeks: 
  - Fork this repo
  - Fix the bug or implement the feature
  - Perform a pull request
2. [Open an issue](https://github.com/GillesC/KU-Leuven-master-thesis-template-FET/issues)

