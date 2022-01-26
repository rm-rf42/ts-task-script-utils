import pytest
from pendulum import now

from task_script_utils.datetime_parser import ts_datetime
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


@pytest.mark.parametrize(
    "input_, iso_format, datetime_iso_format", subseconds_test_cases
)
def test_subseconds(input_, iso_format, datetime_iso_format):
    fmt = "dddd, MMMM Do YYYY hh:mm:ss.SSSSSS A z"
    ts_datetime = from_pendulum_format(input_, fmt, now(), None)
    assert ts_datetime.isoformat() == iso_format
    assert ts_datetime.datetime.isoformat() == datetime_iso_format
