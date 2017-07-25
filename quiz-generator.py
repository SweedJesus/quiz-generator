#!/usr/bin/env python

# TODO:
# - Fix bad-boxes from minipages
#   (https://tex.stackexchange.com/questions/199635/underfull-hbox-badness-10000-message#199638)

import re
import sys
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input",
        help="input problem files",
        nargs="+")
parser.add_argument("-o","--output",
        help="output file (default stdout)",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout)
parser.add_argument("-t","--title",
        help="quiz title",
        metavar="TITLE",
        default="Generic Quiz")
parser.add_argument("-r","--randomize",
        help="randomize problems",
        action="store_true",
        dest="randomize")
args = parser.parse_args()

pattern = re.compile(":::\s*(.*)\s*\n")
problems=[]
if args.input:
    for _path in args.input:
        with open(_path, "r") as _file:
            _content = "\n".join([
                l for l in
                _file.read().splitlines() if l and l[0] != '%'])
            _match = pattern.search(_content)
            _source = _match and _match.group(1) or "Unknown"
            _content = pattern.sub("", _content)
            problems.extend([
                [_source, _problem[0], (len(_problem) == 2) and _problem[1] or None]
                for _problem in [ _qa_pair.split("\n===\n")
                    for _qa_pair in _content.split("\n---\n")]])

if args.randomize:
    random.shuffle(problems)

content_quiz = ""
content_answers = ""
problem_pattern = ("\n\\item[\\hyperlink{{{0}-answer}}{{{0}}}.]"
        "\\hypertarget{{{0}-problem}}{{}}\n\n"
        "{1}\n\\smallskip\n")
answer_pattern = ("\n\\item[\\hyperlink{{{0}-problem}}{{{0}}}.]"
        "\\hypertarget{{{0}-answer}}{{}}"
        "\\textit{{({1})}}\n\n"
        "{2}\n\\smallskip\n")
for i, val in enumerate(problems):
    content_quiz += problem_pattern.format(i+1, val[1])
    if val[2]:
        content_answers += answer_pattern.format(i+1, val[0], val[2])

header=r"""\documentclass[fleqn]{article}
\usepackage[a4paper,margin=1in]{geometry}
\usepackage{multicol}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{resizegather}
\usepackage{xfrac}
\usepackage{lmodern}
\usepackage{textcomp}
\usepackage[utf8]{inputenc}
\usepackage[english]{babel}
\usepackage{hyperref}
\setlength{\parindent}{0pt}
\setlength{\mathindent}{0pt}
\setlength{\delimitershortfall}{0pt}
\def\deriv{\frac{d}{dx}}
\DeclareMathOperator{\arccsc}{arccsc}
\DeclareMathOperator{\arcsec}{arcsec}
\DeclareMathOperator{\arccot}{arccot}
\DeclareMathOperator{\csch}{csch}
\DeclareMathOperator{\sech}{sech}
\DeclareMathOperator{\arcsinh}{arcsinh}
\DeclareMathOperator{\arccosh}{arccosh}
\DeclareMathOperator{\arctanh}{arctanh}
\DeclareMathOperator{\arccsch}{arccsch}
\DeclareMathOperator{\arcsech}{arcsech}
\DeclareMathOperator{\arccoth}{arccoth}
\begin{document}
"""

footer=r"""
\end{document}"""

args.output.write(
        header+
        "\\section*{"+args.title+" (Problems)}\n"+
        "\\begin{multicols*}{2}\n"+
        "\\begin{itemize}\n"+content_quiz+"\\end{itemize}\n"+
        "\\end{multicols*}\n"+
        "\\newpage\n"+
        "\\section*{"+args.title+" (Answers)}\n"+
        "\\begin{multicols*}{2}\n"+
        "\\begin{itemize}\n"+content_answers+"\\end{itemize}\n"+
        "\\end{multicols*}"+
        footer)
