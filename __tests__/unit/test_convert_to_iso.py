import pytest
from task_script_utils.datetime_parser import (
    convert_to_ts_iso8601,
    PipelineConfig,
)

config_with_fold_test_cases = {
    ("2021-11-07T01:30:00 America/New_York", 0, "2021-11-07T05:30:00.000Z"),
    ("2021-11-07T01:30:00.032001 America/New_York", 1, "2021-11-07T06:30:00.032Z"),
    ("2021-11-07T01:30:00.032 America/New_York", 1, "2021-11-07T06:30:00.032Z"),

    #TODO: Confirm these cases
    ("2021-11-07T04:30:00.032001 America/New_York", 1, "2021-11-07T09:30:00.032Z"),
    ("2021-11-07T04:30:00.032 America/New_York", 0, "2021-11-07T09:30:00.032Z")
}


@pytest.mark.parametrize(
    "input_, fold, expected",
    config_with_fold_test_cases
)
def test_convert_to_iso_with_fold(input_, fold, expected):
    config = PipelineConfig(fold=fold, day_first=False)
    result = convert_to_ts_iso8601(input_, config=config)
    assert result == expected