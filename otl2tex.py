import sys
import argparse
import os
import toml

actions = {
    "PART": R"\part{{{}}}",
    "CHAPTER": R"\chapter{{{}}}",
    "SUBSECTION": R"\subsection{{{}}}",
    "SECTION": R"\section{{{}}}"
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

\begin{{document}}

\title{{{title}}}
\author{{{author}}}

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

def file_or_default(filename,default):
    if filename is None:
        return default
    else:
        with open(filename,'r') as f:
            return f.readlines()

def try_load_config(args,path):
    if os.path.exists(os.path.join(os.getcwd(), ".otl2tex.toml")):
        tmp = toml.load(os.path.join(os.getcwd() , ".otl2tex.toml"))
        apply_config(args,tmp)
        print("local config loaded")

def apply_config(args,config):
    for k,v in config.items():
        if k == "title" and args.title is None:
            args.title=v
        elif k == "author" and args.author is None:
            args.author=v
        elif k == "infile" and args.infile is None:
            args.infile=v


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--author", help="author of document", default="me")
    parser.add_argument("-t", "--title", help="title of the document",default="default title")
    parser.add_argument("--preamble", help="filename of the preamble")
    parser.add_argument("--postamble", help="filename of the postamble")
    parser.add_argument("--config", help="defaults to .otl2tex.toml in the local directory")
    parser.add_argument("infile", nargs="?")
    parser.add_argument("outfile", nargs="?")
    args = parser.parse_args()

    try_load_config(args, args.config or os.path.join(os.getcwd(),".otl2tex.toml"))

    if args.infile is None: # TODO: better way to warn if there is no input?
        print("No input file given")
        exit(-1)

    # prepare arguments
    if args.outfile is None:
        args.outfile = args.infile[:-3]+"tex"

    if args.outfile==args.infile:
        print("Error: input-file is output-file, maybe thats not what you intended")
        exit(-1)

    print(args.infile + " -> " + args.outfile)
    
    args.preamble = file_or_default(args.preamble,preamble)
    args.postamble = file_or_default(args.postamble,postamble)


    try:
        with open(args.outfile,'w') as output_file, open(args.infile,'r') as input_file:
            output_file.write(args.preamble.format(author=args.author,title=args.title))
            for line in input_file:
                if relevant_line(line):
                    output_file.write(process(line))
                    output_file.write("\n")
            output_file.write(args.postamble)
    except OSError as e:
        print(f"Error: ", e)
        exit(-1)


if __name__ == "__main__":
    main()
