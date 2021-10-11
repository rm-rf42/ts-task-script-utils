
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

@pytest.mark.parametrize("input, year_first, day_first, expected", two_digit_date_with_config_test_cases)
def test_match_short_date(input, year_first, day_first, expected):
    config_dict = pipeline_configs[(year_first,day_first)]
    config = PipelineConfig.from_dict(config_dict)
    try:
        date_info = DateTimeInfo(input, config)
        result = date_info.short_date
    except Exception as e:
        result = None

    assert result == expected
