import pytest
from task_script_utils.datetime_parser import (
    convert_to_ts_iso8601,
    DatetimeConfig,
)

config_with_fold_test_cases = {
    ("2021-11-07T01:30:00 America/New_York", 0, "2021-11-07T05:30:00Z"),
    ("2021-11-07T01:30:00.000 America/New_York", 0, "2021-11-07T05:30:00.000Z"),
    ("2021-11-07T01:30:00.032001 America/New_York", 1, "2021-11-07T06:30:00.032001Z"),
    ("2021-11-07T01:30:00.032 America/New_York", 1, "2021-11-07T06:30:00.032Z"),
    ("2021-11-07T01:30:00.032", None, "2021-11-07T01:30:00.032"),

    #TODO: Confirm these cases
    ("2021-11-07T04:30:00.032001 America/New_York", 1, "2021-11-07T09:30:00.032001Z"),
    ("2021-11-07T01:30:00.032 America/New_York", 1, "2021-11-07T06:30:00.032Z"),
}


fractional_seconds_test_cases = {
    #Subseconds Cases
    ("2021-11-07T04:30:00 America/New_York", "2021-11-07T09:30:00Z"),
    ("2021-11-07T04:30:00.1 America/New_York", "2021-11-07T09:30:00.1Z"),
    ("2021-11-07T04:30:00.12 America/New_York", "2021-11-07T09:30:00.12Z"),
    ("2021-11-07T04:30:00.123 America/New_York", "2021-11-07T09:30:00.123Z"),
    ("2021-11-07T04:30:00.01230 America/New_York", "2021-11-07T09:30:00.01230Z"),
    ("2021-11-07T04:30:00.123456 America/New_York","2021-11-07T09:30:00.123456Z"),
    ("2021-11-07T04:30:00.00123456 America/New_York","2021-11-07T09:30:00.00123456Z"),
    ("2021-11-07T04:30:00.01 America/New_York","2021-11-07T09:30:00.01Z"),
    ("2021-11-07T04:30:00.010 America/New_York","2021-11-07T09:30:00.010Z"),
    ("2021-11-07T04:30:00.1234567 America/New_York", '2021-11-07T09:30:00.1234567Z'),
}

@pytest.mark.parametrize(
    "input_, fold, expected",
    config_with_fold_test_cases
)
def test_convert_to_iso_with_fold(input_, fold, expected):
    config = DatetimeConfig(fold=fold, day_first=False)
    try:
        result = convert_to_ts_iso8601(input_, config=config)
    except Exception as e:
        result = None
        print(e)
    assert result == expected


@pytest.mark.parametrize(
    "input_, expected",
    fractional_seconds_test_cases
)
def test_convert_to_iso_with_fractional_seconds(input_, expected):

    config = DatetimeConfig(day_first=False)
    try:
        result = convert_to_ts_iso8601(input_, config=config)
    except Exception as e:
        result = None
    assert result == expected