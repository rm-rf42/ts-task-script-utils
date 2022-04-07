# pylint: disable=C0114
# pylint: disable=E0401
import pytest
from task_script_utils.datetime_parser.utils.parsing import parse_with_formats
from task_script_utils.datetime_parser import DatetimeConfig
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError

format_list_with_no_tz_dict_test_cases = {
    "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM ZST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM": None,
}

formats_list = [
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz",
    "dddd, MMMM DD YYYY hh:mm:ss A z",
    "dddd, MMMM Do, YYYY hh:mm:ss A z",
    "dddd, MMMM DD YYYY hh:mm:ss.SSSSSS A z",
    "dddd, MMMM Do, YYYY hh:mm:ss.SSSSSS A z",
]


@pytest.mark.parametrize(
    "input_, expected", format_list_with_no_tz_dict_test_cases.items()
)
def test_parse_with_formats_with_no_tz_dict(input_, expected):
    """Test `parse_with_formats` when no tz_dict is present in datetime_config"""
    if expected is None:
        with pytest.raises(DatetimeParserError):
            parse_with_formats(input_, formats_list, DatetimeConfig())
    else:
        parsed_datetime = parse_with_formats(input_, formats_list, DatetimeConfig())

        if parsed_datetime is None:
            assert parsed_datetime == expected
        else:
            assert parsed_datetime.isoformat() == expected
