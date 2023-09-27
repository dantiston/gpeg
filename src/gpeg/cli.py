#!/usr/bin/env python3.11

import argparse
import sys
import traceback

from typing import Iterable

import pe


def match_yield(expression: str, lines: Iterable[str]) -> Iterable[str]:
    grammar = pe.compile(expression)
    for line in lines:
        if grammar.match(line, flags=pe.MEMOIZE | pe.OPTIMIZE):
            yield line.strip()


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
    return parser
