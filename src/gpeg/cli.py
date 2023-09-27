#!/usr/bin/env python3.11

import argparse
import sys
import traceback

from typing import Iterable
from dataclasses import dataclass

import pe


@dataclass
class GpegArgs:
    line_number: bool = False

    @classmethod
    def from_argparse(cls, args: argparse.Namespace) -> "GpegArgs":
        return GpegArgs(line_number=args.line_number)


def format_match(line: str, n: int, args: GpegArgs) -> str:
    result = line.rstrip()
    if args.line_number:
        result = f"{n}:{result}"
    return result


def match_yield(expression: str, lines: Iterable[str], args: GpegArgs) -> Iterable[str]:
    grammar = pe.compile(expression)
    for n, line in enumerate(lines, start=1):
        # pe.MEMOIZE: give better error messages
        # pe.OPTIMIZE: alter the grammar to improve runtime
        if grammar.match(line, flags=pe.MEMOIZE | pe.OPTIMIZE):
            yield format_match(line, n, args)


def main(args: argparse.Namespace) -> int:
    if args.input is None:
        args.input = sys.stdin.readlines()
    try:
        for match in match_yield(args.expression, args.input):
            print(match)
        return 0
    except Exception as e:
        traceback.print_exception(e)
        return 1


def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "gpeg",
        description="Search with Parsing Expressions: global/parsing expressions/print",
    )
    parser.add_argument("expression", help="The expression to match")
    parser.add_argument(
        "input",
        help="New line separated values to check against the expression, defaults to stdin",
        type=argparse.FileType("r"),
        default=None,
    )
    parser.add_argument(
        "-n",
        "--line-number",
        type=int,
        help=(
            "Each output line is preceded by its relative line number in the file, starting at line 1.  "
            "The line number counter is reset for each file processed.  "
            "This option is ignored if -c, -L, -l, or -q is specified."
        ),
    )
    return parser
