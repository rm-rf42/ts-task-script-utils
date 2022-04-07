import pytest
from pendulum import now

from task_script_utils.datetime_parser.utils import from_pendulum_format


subseconds_test_cases = [
    # raw, TSDatetime.isofromat(), TSDatetime.datetime.isoformat()
    (
        "Sunday, May 26th 2013 12:12:12.1 AM Asia/Kolkata",
        "2013-05-26T00:12:12.1+05:30",
        "2013-05-26T00:12:12.100000+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.0001 AM Asia/Kolkata",
        "2013-05-26T00:12:12.0001+05:30",
        "2013-05-26T00:12:12.000100+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.00100 AM Asia/Kolkata",
        "2013-05-26T00:12:12.00100+05:30",
        "2013-05-26T00:12:12.001000+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.01010001 AM Asia/Kolkata",
        "2013-05-26T00:12:12.01010001+05:30",
        "2013-05-26T00:12:12.010100+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.00120200 AM Asia/Kolkata",
        "2013-05-26T00:12:12.00120200+05:30",
        "2013-05-26T00:12:12.001202+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.10000100 AM Asia/Kolkata",
        "2013-05-26T00:12:12.10000100+05:30",
        "2013-05-26T00:12:12.100001+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.4300345 AM Asia/Kolkata",
        "2013-05-26T00:12:12.4300345+05:30",
        "2013-05-26T00:12:12.430034+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.000000001 AM Asia/Kolkata",
        "2013-05-26T00:12:12.000000001+05:30",
        "2013-05-26T00:12:12+05:30",
    ),
    (
        "Sunday, May 26th 2013 12:12:12.00000000 AM Asia/Kolkata",
        "2013-05-26T00:12:12.00000000+05:30",
        "2013-05-26T00:12:12+05:30",
    ),
]

padding_test_cases = [
    ("1/1/1", "MM/DD/YYYY", "0001-01-01T00:00:00", "0001-01-01T00:00:00"),
    (
        "1/1/1 America/Chicago",
        "MM/DD/YYYY z",
        "0001-01-01T06:00:00Z",
        "0001-01-01T00:00:00-06:00",
    ),
]


@pytest.mark.parametrize(
    "input_, iso_format, datetime_iso_format", subseconds_test_cases
)
def test_subseconds(input_: str, iso_format: str, datetime_iso_format: str):
    fmt = "dddd, MMMM Do YYYY hh:mm:ss.SSSSSS A z"
    ts_datetime_ = from_pendulum_format(input_, fmt, now(), None)
    assert ts_datetime_.isoformat() == iso_format
    assert ts_datetime_.datetime.isoformat() == datetime_iso_format


def test_invalid_format_string():
    """
    If a format string does not contain any datetime tokens, pendulum can not handle it.
    """
    with pytest.raises(TypeError):
        from_pendulum_format(
            "Sunday, May 26th 2013 12:12:12.00000000 AM Asia/Kolkata",
            "GTPgtp",
            now(),
            None,
        )


@pytest.mark.parametrize(
    "input_, format_, expected_ts_format, expected_iso_format", padding_test_cases
)
def test_datetime_padding(input_, format_, expected_ts_format, expected_iso_format):
    """Test for making sure that resulting date is padded as
    YYYY-MM-DD
    """
    ts_datetime_ = from_pendulum_format(input_, format_, None, None)
    assert ts_datetime_.tsformat() == expected_ts_format
    assert ts_datetime_.isoformat() == expected_iso_format
