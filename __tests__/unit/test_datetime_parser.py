import pytest
from task_script_utils.datetime_parser.parser import (
    parse,
    _parse_with_formats,
    _parse_using_dateutils,
)
from task_script_utils.datetime_parser.datetime_config import DatetimeConfig


formats_list = [
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz",
    "dddd, MMMM DD YYYY hh:mm:ss A z",
    "dddd, MMMM Do, YYYY hh:mm:ss A z"
]

tz_dict = {
    "IST": "+05:30",
    "BST": "+01:00"
}

format_list_test_cases = {
    "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM ZST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM BST": "2013-05-26T00:12:12+01:00",
    "Sunday, May 26th 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th, 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
}

parse_with_no_format_list_test_cases = {
    **format_list_test_cases,
    "1:2:32 2021-12-23 AM America/Chicago": "2021-12-23T01:02:32-06:00",
    "1:2:32 2021-12-23 AM +530": "2021-12-23T01:02:32+05:30",
    "May 26 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM IST": "2013-05-26T00:12:12+05:30",
    # Single digit day
    "Thursday, Nov 4 2021 12:12:12 AM Asia/Kolkata": "2021-11-04T00:12:12+05:30",

    # Error Cases:
    # Ambiguity due to unknown abbreviated tz
    # see test_parse() for tz_dict
    "Sunday, May 26th 2013 12:12:12 AM CST": None,
    # Missing Month
    "Sunday, 26 2013 12:12:12 AM Asia/Kolkata": None,
}

format_list_with_no_tz_dict_test_cases = {
    "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM ZST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM": None,
}

dateutil_parser_test_cases = {
    ("11:12:00 21-05-10", True, True): "2021-10-05T11:12:00",
    ("11:12:00 21-05-10", True, False): "2021-05-10T11:12:00",
    ("11:12:00 13-05-10", False, True): "2010-05-13T11:12:00",
    ("11:12:00 13-05-10", False, False): "2010-05-13T11:12:00",
    ("13-05-10", False, False): "2010-05-13T00:00:00",
    ("11:12:00 13-05-10", None, True): None,
    ("11:12:00 13-05-10", True, None): None,
    ("11:12:00 13-05-10", None, None): None
}


@pytest.mark.parametrize(
    "input_, expected",
    dateutil_parser_test_cases.items()
)
def test_date_util_parse(input_, expected):
    datetime_str, year_first, day_first = input_
    config = DatetimeConfig(
        year_first=year_first,
        day_first=day_first
    )

    try:
        result = _parse_using_dateutils(datetime_str, config)
        result = result.isoformat()
    except Exception as e:
        result = None

    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    format_list_test_cases.items()
)
def test_parse_with_formats(input, expected):
    datetime_config_dict = {
        "tz_dict": tz_dict
    }

    datetime_config = DatetimeConfig(**datetime_config_dict)
    parsed_datetime, _ = _parse_with_formats(
        input,
        datetime_config,
        formats_list
    )

    if parsed_datetime is None:
        assert parsed_datetime == expected
    else:
        assert parsed_datetime.isoformat() == expected


@pytest.mark.parametrize(
    "input, expected",
    format_list_with_no_tz_dict_test_cases.items()
)
def test_parse_with_formats_with_no_tz_dict(input, expected):
    parsed_datetime, _ = _parse_with_formats(
        input,
        DatetimeConfig(),
        formats_list
    )

    if parsed_datetime is None:
        assert parsed_datetime == expected
    else:
        assert parsed_datetime.isoformat() == expected


@pytest.mark.parametrize(
    "input, expected",
    parse_with_no_format_list_test_cases.items()
)
def test_parse(input, expected):
    datetime_config_dict = {
        "tz_dict": tz_dict
    }

    datetime_config = DatetimeConfig(**datetime_config_dict)
    try:
        parsed_datetime = parse(
            datetime_str=input,
            config=datetime_config,
        )
        parsed_datetime = parsed_datetime.isoformat()
    except Exception as e:
        parsed_datetime = None

    assert parsed_datetime == expected
