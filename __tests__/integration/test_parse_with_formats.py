from typing import Optional, Sequence
import pytest
from task_script_utils.datetime_parser import DatetimeConfig
from task_script_utils.datetime_parser.parser import parse_with_formats
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError

parse_with_formats_list = [
    # Mix of parseable and unparseable datetime strings for parser.parse_with_formats
    # input_, formats, expected, raises_error
    (
        "2021-12-23T12:12:12Z",
        ["YYYY-MM-DDThh:mm:ssZ"],
        "2021-12-23T12:12:12+00:00",
        False,
    ),
    ("2021/02/3 04:03:00", None, None, True),
    ("3/02/21 04:03:00", None, None, True),
    ("12-12-13T12:12:12Z", None, None, True),
    ("21-11-12T12:12:12Z", None, None, True),
    ("21-11-12T12:12:12Z", None, None, True),
    ("12-13-12T12:12:12Z", None, None, True),
    ("22-12-13T12:12:12Z", None, None, True),
    ("22-12-13T12:12:12Z", None, None, True),
    ("32-32-2002T12:12:12 America/Chicago", None, None, True),
    (
        "3/02/21 04:03:00",
        ["DD/MM/YY hh:mm:ss", "YY/MM/DD hh:mm:ss"],
        "2021-02-03T04:03:00",
        False,
    ),
    ("2021/02/3 04:03:00", ["YYYY/DD/MM hh:mm:ss"], "2021-03-02T04:03:00", False),
    (
        "12-12-13T12:12:12Z",
        ["YY-MM-DDThh:mm:ssZ", "DD-MM-YYThh:mm:ssZ"],
        "2012-12-13T12:12:12+00:00",
        False,
    ),
    (
        "21-11-12T12:12:12Z",
        ["DD-MM-YYThh:mm:ssZ", "YY-MM-DDThh:mm:ssZ"],
        "2012-11-21T12:12:12+00:00",
        False,
    ),
    (
        "21-11-12T12:12:12Z",
        ["DD-MM-YYThh:mm:ssZ", "YY-MM-DDThh:mm:ssZ"],
        "2012-11-21T12:12:12+00:00",
        False,
    ),
    (
        "12-13-12T12:12:12Z",
        ["MM-DD-YYThh:mm:ssZ", "DD-MM-YYThh:mm:ssZ"],
        "2012-12-13T12:12:12+00:00",
        False,
    ),
    (
        "22-12-13T12:12:12Z",
        ["DD-MM-YYThh:mm:ssZ", "YY-MM-DDThh:mm:ssZ"],
        "2013-12-22T12:12:12+00:00",
        False,
    ),
    (
        "22-12-13T12:12:12Z",
        ["YY-MM-DDThh:mm:ssZ", "MM-DD-YYThh:mm:ssZ"],
        "2022-12-13T12:12:12+00:00",
        False,
    ),
    (
        "02-01-2002T12:12:12 America/Chicago",
        ["DD-MM-YYYYThh:mm:ss z", "YYYY-MM-DDThh:mm:ss z"],
        "2002-01-02T12:12:12-06:00",
        False,
    ),
]


@pytest.mark.parametrize(
    "input_, formats, expected, raises_error", parse_with_formats_list
)
def test_parse_with_formats(
    input_: str,
    formats: Optional[Sequence[str]],
    expected: Optional[str],
    raises_error: bool,
):
    print(input_, formats, expected)
    datetime_config = DatetimeConfig()
    if raises_error:
        with pytest.raises(DatetimeParserError):
            parsed_datetime = parse_with_formats(
                datetime_raw_str=input_,
                formats=formats,
                config=datetime_config,
            )
    else:
        parsed_datetime = parse_with_formats(
            datetime_raw_str=input_,
            formats=formats,
            config=datetime_config,
        )
        print(parsed_datetime.isoformat())
        assert parsed_datetime.isoformat() == expected
