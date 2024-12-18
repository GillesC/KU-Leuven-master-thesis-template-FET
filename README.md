This is a master thesis template for the students from the [Faculty of Engineering Technology](https://iiw.kuleuven.be/english). 


## Interesting Resources (ordered according to relevance/importance)

- [LaTeX Workshop](https://github.com/GillesC/LaTeX-Workshop/blob/main/LaTeX_Workshop.pdf)
- [Intro LaTeX](https://github.com/dramco-edu/LaTex)
- [Writing scientific documents in LaTeX](https://github.com/DRAMCO/writing-scientific-papers-in-latex-tips-and-tricks)

## Using the template

Change your campus, language and other information in `main.tex`.

```latex
% Information about your discipline
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\opleiding{discipline name}
\afdeling{specialisation}
\campus{ghenteng}                       % Define your campus and language (append "eng" to load the English template)
                                            % campuses: denayer, geel, gent, groept, brugge
\title{Title Masterproef}
\subtitle{subttile (optionale)}
\forenameA{first name}
\surnameA{last name}
\forenameB{} %keep empty if no 2nd author
\surnameB{} %keep empty if no 2nd author
\academicyear{2023 - 2024}
```

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


## Bugs and extensions
If you find a bug or want to request an extension to the template, you have two options:
1. For the geeks: 
  - Fork this repo
  - Fix the bug or implement the feature
  - Perform a pull request
2. [Open an issue](https://github.com/GillesC/KU-Leuven-master-thesis-template-FET/issues)

