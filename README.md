# otl2tex
A small script to generate a LaTeX-Document from a vim-outliner file

At the moment it extract all lines starting with a colon as LaTeX-lines.
Furthermore, there are some experimental commands/markers. The leading content of the line is ignored.

|Command|Effect|
|-------|------|
|PART …|\part{…}|
|CHAPTER …|\chapter{…}|
|SECTION …|\section{…}|
|SUBSECTION …|\subsection{…}|
