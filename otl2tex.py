import sys

actions = {
    "PART": R"\part{{{}}}",
    "CHAPTER": R"\chapter{{{}}}",
    "SUBSECTION": R"\subsection{{{}}}",
    "SECTION": R"\section{{{}}}"
}

preamble = R"""
\documentclass[a5paper]{scrbook}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[ngerman]{babel}

\begin{document}

%\subject{}
\title{Geschichten}
%\subtitle{}
\author{Ich}

\maketitle

\tableofcontents

"""

postamble = "\n\\end{document}\n"

def process(line):
    line = line.strip()
    if line.startswith(':'):
        line = line[1:]
    else:
        for name,s in actions.items():
            idx = line.find(name)
            if idx>=0:
                line = s.format(line[idx+len(name)+1:])
                break
    return line

def relevant_line(line):
    line = line.strip()
    return (not line
        or line.startswith(':')
        or any([name in line for name in actions]))

def help():
    print("otl2tex input-file [output-file]")

def main():
    if len(sys.argv)<2:
        help()
        exit(0)

    infile = sys.argv[1]
    if len(sys.argv)==3:
        outfile = sys.argv[2]
    else:
        outfile = infile[:-3]+"tex"

    if outfile==infile:
        print("Error: input-file is output-file, maybe thats not what you intended")
        exit(-1)

    try:
        with open(outfile,'w') as output_file, open(infile,'r') as input_file:
            output_file.write(preamble)
            for line in input_file:
                if relevant_line(line):
                    output_file.write(process(line))
                    output_file.write("\n")
            output_file.write(postamble)
    except OSError as e:
        print(f"Error: ", e)
        exit(-1)


if __name__ == "__main__":
    main()
