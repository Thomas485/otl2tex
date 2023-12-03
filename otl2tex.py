from typing_extensions import Annotated
import typer
import os

actions = {
    "PART": R"\part{{{}}}",
    "CHAPTER": R"\chapter{{{}}}",
    "SUBSECTION": R"\subsection{{{}}}",
    "SECTION": R"\section{{{}}}",
    "NAME": r"""\directlua{{
      names[\"{name}\"] = {{
        nominative= \"{nom}\",
        genitive= \"{gen}\",
      }}
    }}""",
}

preamble = R"""
\documentclass[a5paper]{{scrbook}}
\usepackage[ngerman]{{babel}}
\usepackage{{ifluatex}}
\ifluatex
\usepackage{{fontspec}}
\else
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\fi

\usepackage{{luacode}}

\begin{{luacode*}}
  names={{}}
\end{{luacode*}}

\newcommand\nom[1]{{%
\luaexec{{
  if names and names.#1 and names.#1.nominative then
    tex.print(names.#1.nominative)
  else
  error('Error: Can not find nominative for name: ' ..  '#1')
  end
}}}}
\newcommand\gen[1]{{%
\luaexec{{
  if names and names.#1 and names.#1.genitive then
    tex.print(names.#1.genitive)
  else
  error('Error: Can not find genitive for name: ' ..  '#1')
  end
}}}}

\begin{{document}}

\title{{{title}}}
\author{{{author}}}

\maketitle

\tableofcontents

"""

postamble = "\n\\end{document}\n"


def map_name_section(line):
    lst = line.split(" ")
    if len(lst) == 3:
        return lst
    else:
        return None


def extract_name(data, s):
    lst = map_name_section(data)
    if lst is None:
        print("Error: Wrong syntax for NAME:", data)
        exit(-1)
    else:
        return s.format(name=lst[0], nom=lst[1], gen=lst[2])


def process(line):
    line = line.strip()
    if line.startswith(":"):
        line = line[1:]
    else:
        for name, s in actions.items():
            idx = line.find(name)
            if idx >= 0:
                data = line[idx + len(name) + 1:]
                if name == "NAME":
                    line = extract_name(data, s)
                else:
                    line = s.format(data)
                break
    return line


def relevant_line(line):
    line = line.strip()
    return not line or line.startswith(":") or any([name in line for name in actions])


def main(infile: str,
         outfile: str,
         author: Annotated[str, typer.Option("--author", "-a")] = "Me",
         title: Annotated[str, typer.Option("--title", "-t")] = "My Title",
         quiet: Annotated[bool, typer.Option("--quiet", "-q")] = False,
         pdf: Annotated[bool, typer.Option("--pdf")] = False,
         ):

    if outfile == infile:
        print("Error: input-file is output-file, maybe thats not what you intended")
        exit(-1)

    if not quiet:
        print(infile + " -> " + outfile)

    with open(outfile, "w") as output_file, open(infile, "r") as input_file:
        output_file.write(preamble.format(
            author=author, title=title))
        for line in input_file:
            if relevant_line(line):
                output_file.write(process(line))
                output_file.write("\n")
        output_file.write(postamble)

    if pdf:
        os.system(f"latexmk  -pdf -pdflatex=lualatex {outfile}")


if __name__ == "__main__":
    try:
        typer.run(main)
    except OSError as e:
        print("Error: ", e)
        exit(-1)
