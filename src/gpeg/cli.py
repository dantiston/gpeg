#!/usr/bin/env python3.11

import argparse
import sys
import traceback

import pe


def main(args: argparse.Namespace) -> int:
    if args.input is None:
        args.input = sys.stdin.readlines()
    try:
        grammar = pe.compile(args.expression)
        for line in args.input:
            if grammar.match(line, flags=pe.MEMOIZE):
                print(line.strip())
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
