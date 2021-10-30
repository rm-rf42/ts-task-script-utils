import pytest
from task_script_utils.datetime_parser.parser import (
    parse,
    parse_with_formats,
    parse_using_dateutils,
)
from task_script_utils.datetime_parser.pipeline_config import PipelineConfig


formats_list = [
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz"
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
}

format_list_with_no_tz_dict_test_cases = {
    "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM ZST Asia/Kolkata": None,
    "Sunday, May 26th 2013 12:12:12 AM Asia/Kolkata": "2013-05-26T00:12:12+05:30",
    "Sunday, May 26th 2013 12:12:12 AM": None
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
    config = PipelineConfig(
        year_first=year_first,
        day_first=day_first
    )

    try:
        result = parse_using_dateutils(datetime_str, config)
        result = result.isoformat()
    except Exception as e:
        result = None

    assert result == expected


@pytest.mark.parametrize(
    "input, expected",
    format_list_test_cases.items()
)
def test_parse_with_formats(input, expected):
    pipe_config_dict = {
        "tz_dict": tz_dict
    }

    pipeline_config = PipelineConfig(**pipe_config_dict)
    parsed_datetime, _ = parse_with_formats(
        input,
        pipeline_config,
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
    parsed_datetime, _ = parse_with_formats(
        input,
        PipelineConfig(),
        formats_list
    )

    if parsed_datetime is None:
        assert parsed_datetime == expected
    else:
        assert parsed_datetime.isoformat() == expected


@pytest.mark.parametrize(
    "input, expected",
    format_list_test_cases.items()
)
def test_parse(input, expected):
    pipe_config_dict = {
        "tz_dict": tz_dict
    }

    pipeline_config = PipelineConfig(**pipe_config_dict)
    try:
        parsed_datetime = parse(
            datetime_str=input,
            config=pipeline_config,
        )
        assert parsed_datetime.isoformat() == expected
    except Exception as e:
        parsed_datetime = None
        assert parsed_datetime == expected