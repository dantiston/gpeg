#!/usr/bin/env python3.11

import sys

from src.gpep.cli import main, main_parser

if __name__ == "__main__":
    parser = main_parser()
    args = parser.parse_args()
    sys.exit(main(args))
