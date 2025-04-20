# otl2tex
A small script to generate a LaTeX-Document from a vim-outliner file

At the moment it extract all lines starting with a colon as LaTeX-lines.
Furthermore, there are some commands/markers. The leading content of these lines is ignored.

For languages other than German you need to change the latex-preamble in the python file.

|Command|Effect|Note|
|-------|------|----|
|PART …|\part{…}||
|CHAPTER …|\chapter{…}||
|SECTION …|\section{…}||
|SUBSECTION …|\subsection{…}||
|AUTHOR …| \author{…}| needs to be before TITLE|
|TITLE …| \title{…} \maketitle||
|TOC| \tableofcontents| inserts the table of contents|
