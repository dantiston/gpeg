#!/usr/bin/env python3.11

import argparse
import sys


def main(args: argparse.Namespace) -> int:
    return 0


def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        "gpeg",
        description="Search with Parsing Expressions: global/parsing expressions/print",
    )
    parser.add_argument("grammar", help="The grammar to match")
    parser.add_argument(
        "input",
        help="New line separated values to check against the grammar, defaults to stdin",
        default=sys.stdin,
    )
    return parser
