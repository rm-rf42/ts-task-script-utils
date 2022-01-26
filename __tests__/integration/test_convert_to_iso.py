import pytest
from task_script_utils.datetime_parser import (
    convert_to_ts_iso8601,
    DatetimeConfig,
)
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError

config_with_fold_test_cases = {
    # Cases where fold is relevant
    ("2021-11-07T01:30:00.032 America/New_York", 1, "2021-11-07T06:30:00.032Z"),
    ("2021-11-7T01:30:00.032 America/New_York", 1, "2021-11-07T06:30:00.032Z"),
    ("2021-11-07T01:30:00.032 America/New_York", 0, "2021-11-07T05:30:00.032Z"),
    ("2021-10-31T01:15:00 Europe/London", 1, "2021-10-31T01:15:00Z"),
    ("2021-10-31T01:15:00 Europe/London", 0, "2021-10-31T00:15:00Z"),
    ("2021-10-31T02:45:00 Europe/Rome", 1, "2021-10-31T01:45:00Z"),
    ("2021-10-31T02:45:00 Europe/Rome", 0, "2021-10-31T00:45:00Z"),
    # On a date when the fold is irrelevant, it is ignored
    ("2021-11-06T01:30:00 America/New_York", 0, "2021-11-06T05:30:00Z"),
    ("2021-11-06T01:30:00 America/New_York", 1, "2021-11-06T05:30:00Z"),
    ("2021-11-08T01:30:00 America/New_York", 1, "2021-11-08T06:30:00Z"),
    ("2021-11-08T01:30:00 America/New_York", 0, "2021-11-08T06:30:00Z"),
    # Test cases when fold is None but is required to parse
    # datetime with no ambiguity. Hence these are error cases.
    ("2021-10-31T02:45:00 Europe/Rome", None, None),
    ("2021-11-07T01:30:00.032 America/New_York", None, None),
    # Fold is None and is not needed to parse datetime
    (
        "2021-11-07T04:30:00.032001 America/New_York",
        None,
        "2021-11-07T09:30:00.032001Z",
    ),
}


fractional_seconds_test_cases = {
    # Subseconds Cases
    ("2021-11-07T04:30:00 America/New_York", "2021-11-07T09:30:00Z"),
    ("2021-11-07T04:30:00.1 America/New_York", "2021-11-07T09:30:00.1Z"),
    ("2021-11-07T04:30:00.12 America/New_York", "2021-11-07T09:30:00.12Z"),
    ("2021-11-07T04:30:00.123 America/New_York", "2021-11-07T09:30:00.123Z"),
    ("2021-11-07T04:30:00.01230 America/New_York", "2021-11-07T09:30:00.01230Z"),
    ("2021-11-07T04:30:00.123456 America/New_York", "2021-11-07T09:30:00.123456Z"),
    ("2021-11-07T04:30:00.00123456 America/New_York", "2021-11-07T09:30:00.00123456Z"),
    ("2021-11-07T04:30:00.01 America/New_York", "2021-11-07T09:30:00.01Z"),
    ("2021-11-07T04:30:00.010 America/New_York", "2021-11-07T09:30:00.010Z"),
    ("2021-11-07T04:30:00.1234567 America/New_York", "2021-11-07T09:30:00.1234567Z"),
}

datetime_with_config_tests = {
    # input, year_first, day_first, expected(TS datetime format)
    ("01/02/03T04:30:00 America/New_York", False, True, "2003-02-01T09:30:00Z"),
    ("01/02/3T04:30:00 America/New_York", False, True, "2003-02-01T09:30:00Z"),
    ("1/2/3T4:30:00 America/New_York", False, True, "2003-02-01T09:30:00Z"),
    ("1/2/3T4:3:00 America/New_York", False, True, "2003-02-01T09:03:00Z"),
    ("01/02/13T04:03:00 America/New_York", False, True, "2013-02-01T09:03:00Z"),
    ("01/02/03 04:03:00 America/New_York", True, True, "2001-03-02T09:03:00Z"),
    ("01/02/03 04:03:00 America/New_York", False, True, "2003-02-01T09:03:00Z"),
    ("01/02/03 04:03:00 America/New_York", None, True, "2003-02-01T09:03:00Z"),
    ("1/02/03 04:03:00 America/New_York", True, False, "2001-02-03T09:03:00Z"),
    ("01/02/03 04:03:00 America/New_York", False, False, "2003-01-02T09:03:00Z"),
    ("01/02/03 04:03:00 America/New_York", None, False, None),
    ("01/02/03 04:03:00.0 America/New_York", True, None, "2001-02-03T09:03:00.0Z"),
    ("01/02/03 04:03:00 America/New_York", False, None, None),
    ("01/2/3 04:03:00 America/New_York", None, None, None),
    ("13/02/03 04:03:00 America/New_York", True, True, "2013-03-02T09:03:00Z"),
    (
        "13/2/03 04:03:00.43500 America/New_York",
        False,
        True,
        "2003-02-13T09:03:00.43500Z",
    ),
    ("13/02/03 04:03:00 America/New_York", None, True, "2003-02-13T09:03:00Z"),
    ("13/02/03 04:03:00 +05:30", True, False, "2013-02-02T22:33:00Z"),
    ("13/02/3 04:03:00 America/New_York", False, False, None),
    ("13-02-03 04:03:00 America/New_York", None, False, "2013-02-03T09:03:00Z"),
    ("13/02/03 04:03:00 America/New_York", True, None, "2013-02-03T09:03:00Z"),
    ("13/2/03 04:03:00 America/New_York", False, None, "2003-02-13T09:03:00Z"),
    ("13/02/03 04:03:00 America/New_York", None, None, None),
    ("01/15/11 04:03:00 America/New_York", None, True, None),
    ("01/15/11 04:03:00 America/New_York", True, False, None),
    ("12/13/03 04:03:00 America/New_York", None, False, "2003-12-13T09:03:00Z"),
    (
        "2021.11.07 04:03:00.00045000 America/New_York",
        None,
        False,
        "2021-11-07T09:03:00.00045000Z",
    ),
    ("2021/11/07 04:03:00 America/New_York", None, True, "2021-07-11T08:03:00Z"),
    ("11\\12\\2021 04:03:00 America/New_York", None, True, "2021-12-11T09:03:00Z"),
    ("2021/11/07 04:03:00 America/New_York", None, None, "2021-11-07T09:03:00Z"),
    ("2021/32/07 04:03:00 America/New_York", None, True, None),
    ("2021/11/14 04:03:00 America/New_York", None, True, None),
    ("2021.11.7 04:03:00 America/New_York", None, False, "2021-11-07T09:03:00Z"),
}

datetime_strings_with_and_without_Z = {
    # (input, datetime_formats_lists, expected)
    ("2021-12-13T13:00:00.1234567Z", (), "2021-12-13T13:00:00.1234567Z"),
    ("2021-12-13T13:00:00.1234567 Z", (), "2021-12-13T13:00:00.1234567Z"),
    ("2021-12-13T13:00:00.1234567", (), "2021-12-13T13:00:00.1234567"),
    ("13:00:00.1234567 Z 2021-12-13 ", (), "2021-12-13T13:00:00.1234567Z"),
    ("13:00:00.1234567Z 2021-12-13 ", (), "2021-12-13T13:00:00.1234567Z"),
    ("21-12-12T13:00:00", ("YY-MM-DDTHH:mm:ss",), "2021-12-12T13:00:00"),
    ("21-12-12T13:00:00Z", ("YY-MM-DDTHH:mm:ssZ",), "2021-12-12T13:00:00Z"),
    ("21-12-12T13:00:00 Z", ("YY-MM-DDTHH:mm:ss Z",), "2021-12-12T13:00:00Z"),
}


@pytest.mark.parametrize("input_, fold, expected", config_with_fold_test_cases)
def test_convert_to_iso_with_fold(input_, fold, expected):
    config = DatetimeConfig(fold=fold, day_first=False)
    try:
        result = convert_to_ts_iso8601(input_, config=config)
    except DatetimeParserError as e:
        result = None
    assert result == expected


@pytest.mark.parametrize("input_, expected", fractional_seconds_test_cases)
def test_convert_to_iso_with_fractional_seconds(input_, expected):

    config = DatetimeConfig(day_first=False)
    try:
        result = convert_to_ts_iso8601(input_, config=config)
    except DatetimeParserError as e:
        result = None
    assert result == expected


@pytest.mark.parametrize(
    "input_, year_first, day_first, expected", datetime_with_config_tests
)
def test_convert_to_ts_format_for_padding(input_, year_first, day_first, expected):
    config = DatetimeConfig(year_first=year_first, day_first=day_first)
    try:
        result = convert_to_ts_iso8601(input_, config=config)
    except DatetimeParserError as e:
        result = None
    assert result == expected


@pytest.mark.parametrize(
    "input_, dt_formats, expected", datetime_strings_with_and_without_Z
)
def test_datetime_str_with_Z(input_, dt_formats, expected):
    try:
        result = convert_to_ts_iso8601(input_, formats_list=list(dt_formats))
    except DatetimeParserError as e:
        print(str(e))
        result = None
    assert result == expected