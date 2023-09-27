#!/usr/bin/env python3.11

import pytest

from src.gpeg.cli import match_yield, GpegArgs


DEFAULT_ARGS = GpegArgs()


@pytest.mark.parametrize(
    "expression,values,expected",
    [
        # Basic
        ("[0-9]", ["1"], ["1"]),
        ("[0-9]", ["a"], []),
        ("[0-9]", ["1", "a"], ["1"]),
        ("[2-9]", ["1", "a"], []),
        ("[0-9]+ [.] [0-9]+", ["1.0", "123.456"], ["1.0", "123.456"]),
        ("[0-9]+ [.] [0-9]+", ["1.0", "1", "abc", "123.456"], ["1.0", "123.456"]),
        # Operators
        ("'1' / '2'", ["1", "2", "3"], ["1", "2"]),
        # ("'1' &'2'", ["1", "1 2", "2"], ["1 2"]),
        # ("'1' !'2'", ["1", "1 2", "2"], ["1", "2"]),
        # Recursion
        ("top <- '(' top* ')'", ["()"], ["()"]),
        ("top <- '(' top* ')'", ["(())"], ["(())"]),
        ("top <- '(' top* ')'", ["(()())"], ["(()())"]),
        ("top <- '(' top* ')'", [")"], []),
        ("top <- '(' top* ')'", ["("], []),
        ("top <- '(' top* ')'", ["(()"], []),
        ("top <- '(' top* ')'", ["(("], []),
        # Full
        (
            "\n".join(
                [
                    "date_time <- offset_date_time / local_date_time / local_date / local_time",
                    "offset_date_time <- date time_delim time offset",
                    "local_date_time <- date time_delim time",
                    "local_date <- date",
                    "local_time <- time",
                    "time_delim <- [Tt ]",
                    'offset <- [-+] hour ":" minute / [Zz]',
                    'time <- hour ":" minute ":" second secfrac?',
                    "hour <- DIGIT2",
                    "minute <- DIGIT2",
                    "second <- DIGIT2",
                    'secfrac <- "." DIGIT+',
                    'date <- year "-" month "-" day',
                    "year <- DIGIT4",
                    "month <- DIGIT2",
                    "day <- DIGIT2",
                    "DIGIT <- [0-9]",
                    "DIGIT2 <- ~( DIGIT DIGIT )",
                    "DIGIT4 <- ~( DIGIT2 DIGIT2 )",
                ]
            ),
            [
                "1979-05-27T00:32:00-07:00",
                "1979-05-27T07:32:00",
                "1979-05-27",
                "07:32:00",
                "007:32:00",
                "Good morning",
            ],
            [
                "1979-05-27T00:32:00-07:00",
                "1979-05-27T07:32:00",
                "1979-05-27",
                "07:32:00",
            ],
        ),
    ],
)
def test_expression(expression: str, values: list[str], expected: list[str]) -> None:
    actual: list[str] = list(match_yield(expression, values, DEFAULT_ARGS))
    assert actual == expected


@pytest.mark.parametrize(
    "expression,values,args,expected",
    [
        ("[0-9]", ["1"], GpegArgs(line_number=True), ["1:1"]),
        ("[0-9]", ["1", "2"], GpegArgs(line_number=True), ["1:1", "2:2"]),
        ("[0-9]", ["1", "a", "2"], GpegArgs(line_number=True), ["1:1", "3:2"]),
    ],
)
def test_args(
    expression: str, values: list[str], args: GpegArgs, expected: list[str]
) -> None:
    actual: list[str] = list(match_yield(expression, values, args))
    assert actual == expected
