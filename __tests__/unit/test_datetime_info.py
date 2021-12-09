
import pytest
from task_script_utils.datetime_parser.datetime_info import DateTimeInfo
from task_script_utils.datetime_parser.datetime_config import DatetimeConfig
from task_script_utils.datetime_parser import tz_dicts
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError


datetime_configs = {
    (None, None): {},
    (True, None): {
        "year_first": True,
    },
    (True, True): {
        "year_first": True,
        "day_first": True
    },
    (True, False): {
        "year_first": True,
        "day_first": False
    },
    (False, None): {
        "year_first": False,
    },
    (False, True): {
        "year_first": False,
        "day_first": True
    },
    (False, False): {
        "year_first": False,
        "day_first": False
    },
    (None, True): {
        "day_first": True
    },
    (None, False): {
        "day_first": False
    }
}

two_digit_date_with_config_test_cases = [
    # input, year_first, day_first, expected
    # Expected date format = YYYY-MM-DD
    ("01/02/03", True, True, "2001-03-02"),
    ("01/02/03", False, True, "2003-02-01"),
    ("01/02/03", None, True, "2003-02-01"),
    ("1/02/03", True, False, "2001-02-03"),
    ("01/02/03", False, False, "2003-01-02"),
    ("01/02/03", None, False, None),
    ("01/02/03", True, None, "2001-02-03"),
    ("01/02/03", False, None, None),
    ("01/2/3", None, None, None),
    ("13/02/03", True, True, "2013-03-02"),
    ("13/2/03", False, True, "2003-02-13"),
    ("13/02/03", None, True, "2003-02-13"),
    ("13/02/03", True, False, "2013-02-03"),
    ("13/02/3", False, False, None),
    ("13-02-03", None, False, "2013-02-03"),
    ("13/02/03", True, None, "2013-02-03"),
    ("13/2/03", False, None, "2003-02-13"),
    ("13/02/03", None, None, None),
    ("01/15/11", None, True, None),
    ("01/15/11", True, False, None),
    ("12/13/03", None, False, "2003-12-13"),
    ("2021.11.07", None, False,'2021-11-07'),
    ("2021/11/07", None, True,'2021-07-11'),
    ("11\\12\\2021", None, True, "2021-12-11"),
    ("2021/11/07", None, None, None),
    ("2021/32/07", None, True, None),
    ("2021/11/14", None, True, None),
    ("2021.11.7", None, False,'2021-11-07')
]

# Test them with year_first
# The goal is to test regex
regex_test_cases = [
    ("1:2:32 20-12-1 AM America/Chicago", "01-12-2020 01:02:32 AM America/Chicago"),
    ("1:2:32 20-11-1 -1 AM America/Chicago", "01-11-2020 01:02:32 AM -01:00 America/Chicago"),
    ("2021-11-13 12:34:43.442", "13-11-2021 12:34:43.442"),
    ("Date: 2021-11-13\nTime: 13:11:13 (UTC+2)", "13-11-2021 13:11:13 +02:00"),
    ("Date: 12-9-1, Time: 17:18:48", "01-09-2012 17:18:48"),
    ("2018-13-09 16:15+2 PM", "13-09-2018 16:15:00 +02:00"),
    ("2018-13-09T11:12:23.000-05:30", "13-09-2018 11:12:23.000 -05:30"),
    ("2018-13-09 11:12:23.000+05:30", "13-09-2018 11:12:23.000 +05:30"),
    ("2018-13-09T01:15+14 PM", "13-09-2018 01:15:00 PM +14:00"),
    ("2018-13-09T16:15-14 PM", "13-09-2018 16:15:00 -14:00"),
    ("2018-13-09T16:15 +05:30 PM", "13-09-2018 16:15:00 +05:30"),
    ("2018-13-09T16:15+5:30 PM", "13-09-2018 16:15:00 +05:30"),
    ("2018-13-09T16:15-0530 PM", "13-09-2018 16:15:00 -05:30"),
    ("2018-13-09T16:15 CST PM", "13-09-2018 16:15:00 -06:00"),
    ("2018-13-09T16:15:4.15 +05:30 PM", "13-09-2018 16:15:04.15 +05:30"),


    #Error Cases
    ("2018-13-09T16:15:4:15 +05:30 PM", None),
    ("2021-11-13 12:67:43.2322222", None),
    ("2021-11-13 25:34:43.23", None),
    ("2021-11-13 12:67:43.23", None),
    ("2021-11-13 12:34:67.23", None),
    ("202-11-13 12:34:09.23", None),
    ("2020-40-40 12:34:09.23", None),
    ("2018-13-09T16:15+5:3 PM", None),
    ("2018-13-09T16:15+05332 PM", None),
    ("1:2:32 20-13-1 AM America/Chicago", None),
    ("2018-13-09T16:15+2 AM", None) # hrs = 16 but meridiem=AM
]


@pytest.mark.parametrize("input, year_first, day_first, expected", two_digit_date_with_config_test_cases)
def test_match_short_date(input, year_first, day_first, expected):
    config_dict = datetime_configs[(year_first, day_first)]
    config = DatetimeConfig(**config_dict)
    try:
        date_info = DateTimeInfo(input, config)
        result = date_info._date_str
    except DatetimeParserError as e:
        result = None

    assert result == expected


@pytest.mark.parametrize("input, expected", regex_test_cases)
def test_regex_parsing(input, expected):
    config = {
        "year_first": True,
        "tz_dict": tz_dicts.USA
        }
    year_first = DatetimeConfig(**config)
    try:
        d = DateTimeInfo(input, year_first)
        parsed_datetime = d.dtstamp
    except DatetimeParserError as e:
        parsed_datetime = None

    assert parsed_datetime == expected

