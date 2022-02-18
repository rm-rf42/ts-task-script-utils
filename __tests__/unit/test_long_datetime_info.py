import pytest
from task_script_utils.datetime_parser.datetime_info import LongDateTimeInfo
from task_script_utils.datetime_parser.datetime_config import DatetimeConfig
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError


long_datetime_test_cases = {
    "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM ZST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM BST": "2013-05-26T00:12:12+01:00",
    "Sunday, May 26th 2013 12:12:12.00100 AM BST": "2013-05-26T00:12:12.00100+01:00",
    "Sunday, May 26th 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th, 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26 2013 12:12:12.5677 AM Asia/Kolkata": "2013-05-26T00:12:12.5677+05:30",
    "Sunday, May 26 2013 12:12:12.0000 AM Asia/Kolkata": "2013-05-26T00:12:12.0000+05:30",
    "Sunday, May 26th 2013 12:12:12.5677 AM Asia/Kolkata": "2013-05-26T00:12:12.5677+05:30",
    "Sunday, May 26th 2013 12:12:12.0001 AM Asia/Kolkata": "2013-05-26T00:12:12.0001+05:30",
}


@pytest.mark.parametrize("input_, expected", long_datetime_test_cases.items())
def test_long_datetime_info(input_, expected):
    tz_dict = {"IST": "+05:30", "BST": "+01:00"}
    config = DatetimeConfig(year_first=None, day_first=None, tz_dict=tz_dict)
    try:
        date_info = LongDateTimeInfo(input_, config)
        result = date_info.datetime
        if result is not None:
            result = result.isoformat()
    except DatetimeParserError as e:
        result = None

    assert result == expected
