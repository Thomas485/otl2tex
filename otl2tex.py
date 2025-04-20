import os
import sys

actions = {
    "AUTHOR": R"\author{{{}}}",
    "TITLE": R"\title{{{}}} \maketitle",
    "TOC": R"\tableofcontents",
    "PART": R"\part{{{}}}",
    "CHAPTER": R"\chapter{{{}}}",
    "SUBSECTION": R"\subsection{{{}}}",
    "SECTION": R"\section{{{}}}",
}

preamble = R"""
\documentclass[a5paper]{{scrbook}}
\usepackage[ngerman]{{babel}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}

\begin{{document}}

"""

postamble = "\n\\end{document}\n"


def process(line):
    line = line.strip()
    if line.startswith(":"):
        line = line[1:]
    else:
        for name, s in actions.items():
            idx = line.find(name)
            if idx >= 0:
                data = line[idx + len(name) + 1:]
                line = s.format(data)
                break
    return line


def relevant_line(line):
    line = line.strip()
    return not line or line.startswith(":") or any([name in line for name in actions])


def main():
    # parse cli flags
    infile = ""
    outfile = ""
    author = "Me"
    title = "My Title"
    quiet = False
    pdf = False

    if len(sys.argv) < 3:
        print("missing positional arguments: infile and outfile required")
    elif len(sys.argv) > 3:
        i= 1
        while i < len(sys.argv):
            if sys.argv[i] == "--quiet" or sys.argv[i] == "-q":
                quiet = True
                i+=1
                continue
            if sys.argv[i] == "--pdf" or sys.argv[i] == "-pdf":
                pdf = True
                i+=1
                continue

            if not infile:
                infile = sys.argv[i]
                i+=1
                continue
            if not outfile:
                outfile = sys.argv[i]
                i+=1
                continue

            print("Unknown additional argument:", sys.argv[i])
            return

    # proceed
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
        os.system(f"latexmk -pdf {outfile}")


if __name__ == "__main__":
    main()
