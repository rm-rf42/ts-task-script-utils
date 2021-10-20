
import pytest
from task_script_utils.datetime_parser.datetime_info import DateTimeInfo
from task_script_utils.datetime_parser.pipeline_config import PipelineConfig

pipeline_configs = {
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
    #input, year_first, day_first, expected
    ("01/02/03", True, True, "2001-03-02"),
    ("01/02/03", False, True, "2003-02-01"),
    ("01/02/03", None, True, "2003-02-01"),
    ("01/02/03", True, False, "2001-02-03"),
    ("01/02/03", False, False, "2003-01-02"),
    ("01/02/03", None, False, "2003-01-02"),
    ("01/02/03", True, None, None),
    ("01/02/03", False, None, None),
    ("01/02/03", None, None, None),
    ("13/02/03", True, True, "2013-03-02"),
    ("13/02/03", False, True, "2003-02-13"),
    ("13/02/03", None, True, "2003-02-13"),
    ("13/02/03", True, False, "2013-02-03"),
    ("13/02/03", False, False, None),
    ("13/02/03", None, False, None),
    ("13/02/03", True, None, "2013-02-03"),
    ("13/02/03", False, None, "2003-02-13"),
    ("13/02/03", None, None, None)
]


# Test them with year_first
# The goal is to test regex
regex_test_cases = [
    ("1:2:32 20-13-1 AM America/Chicago", "13-01-2020 1:2:32 AM -05:00"),
    ("1:2:32 20-13-1 -1 AM America/Chicago", "13-01-2020 1:2:32 AM -01:00"),
    ("2021-11-13 12:34:43.442", "13-11-2021 12:34:43.442"),
    ("Date: 2021-11-13\nTime: 13:11:13 (UTC+2)", "13-11-2021 13:11:13 +02:00"),
    ("Date: 12-13-1, Time: 17:18:48", "13-01-2012 17:18:48"),
    ("2018-13-09 16:15+2 PM", "13-09-2018 16:15:00 +02:00"),
    ("2018-13-09T16:15+2 AM", "13-09-2018 16:15:00 +02:00"),
    ("2018-13-09T11:12:23.000-05:30", "13-09-2018 11:12:23.000 -05:30"),
    ("2018-13-09 11:12:23.000+05:30", "13-09-2018 11:12:23.000 +05:30"),
    ("2018-13-09T01:15+14 PM", "13-09-2018 01:15:00 PM +14:00"),
    ("2018-13-09T16:15+14 PM", "13-09-2018 16:15:00 +14:00")
]



@pytest.mark.parametrize("input, year_first, day_first, expected", two_digit_date_with_config_test_cases)
def test_match_short_date(input, year_first, day_first, expected):
    config_dict = pipeline_configs[(year_first, day_first)]
    config = PipelineConfig(**config_dict)
    try:
        date_info = DateTimeInfo(input, config)
        date_info.parse()
        result = date_info.short_date
    except Exception as e:
        s = str(e)
        result = None

    assert result == expected

@pytest.mark.parametrize("input, expected", regex_test_cases)
def test_regex_parsing(input, expected):
    year_first = PipelineConfig(**{"year_first": True})
    d = DateTimeInfo(input, year_first)
    d.parse()
    assert d.dtstamp == expected
