#!/usr/bin/env python3.11

import argparse
import sys
import traceback

from typing import Iterable
from dataclasses import dataclass

import pe


@dataclass
class GpegArgs:
    after: int = 0
    before: int = 0
    line_number: bool = False

    @classmethod
    def from_argparse(cls, args: argparse.Namespace) -> "GpegArgs":
        return GpegArgs(
            after=max(args.after_context or 0, args.context or 0),
            before=max(args.before_context or 0, args.context or 0),
            line_number=args.line_number,
        )


def format_match(line: str, n: int, args: GpegArgs, delimiter: str = ":") -> str:
    result = line.rstrip()
    if args.line_number:
        result = f"{n}{delimiter}{result}"
    return result


def match_yield(expression: str, lines: Iterable[str], args: GpegArgs) -> Iterable[str]:
    buffer: list[str] = []
    grammar = pe.compile(expression)
    after_context_count = 0
    for n, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        # pe.MEMOIZE: give better error messages
        # pe.OPTIMIZE: alter the grammar to improve runtime
        if grammar.match(line, flags=pe.MEMOIZE | pe.OPTIMIZE):
            yield from (
                format_match(buffer_line, n + i, args, "-")
                for i, buffer_line in enumerate(buffer, start=-len(buffer))
            )
            yield format_match(line, n, args)
            after_context_count = args.after
        elif after_context_count > 0:
            after_context_count -= 1
            yield format_match(line, n, args, "-")
        if args.before > 0:
            buffer.append(line)
            buffer = buffer[-args.before :]


def main(args: argparse.Namespace) -> int:
    if args.input is None:
        args.input = sys.stdin.readlines()
    try:
        for match in match_yield(
            args.expression, args.input, GpegArgs.from_argparse(args)
        ):
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
        action="store_true",
        help=(
            "Each output line is preceded by its relative line number in the file, starting at line 1.  "
            "The line number counter is reset for each file processed."
        ),
    )
    parser.add_argument(
        "-A",
        "--after-context",
        type=int,
        default=0,
        help="Print num lines of trailing context after each match.",
    )
    parser.add_argument(
        "-B",
        "--before-context",
        type=int,
        default=0,
        help="Print num lines of leading context before each match.",
    )
    parser.add_argument(
        "-C",
        "--context",
        type=int,
        help=(
            "Print num lines of leading and trailing context surrounding each match."
        ),
    )
    return parser
