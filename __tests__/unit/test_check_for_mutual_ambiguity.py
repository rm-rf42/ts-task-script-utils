import pytest
from pendulum import datetime as pendulum_datetime
from task_script_utils.datetime_parser import DatetimeConfig
from task_script_utils.datetime_parser.parser import parse, parse_with_formats
from task_script_utils.datetime_parser.parser_exceptions import (
    AmbiguousDatetimeFormatsError,
)

empty_formats = []

ambiguous_formats = [
    "MM/DD/YYYY hh:mm:ss A z",
    "DD/MM/YYYY hh:mm:ss A z",
]

ambiguous_formats_short_year = [
    "MM/DD/YY hh:mm:ss A z",
    "YY/MM/DD hh:mm:ss A z",
]

ambiguous_formats_with_subseconds = [
    "MM/DD/YYYY hh:mm:ss.SSSSSS A z",
    "DD/MM/YYYY hh:mm:ss.SSSSSS A z",
]

unambiguous_formats = [
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz",
    "dddd, MMMM DD YYYY hh:mm:ss A z",
    "dddd, MMMM Do, YYYY hh:mm:ss A z",
    "dddd, MMMM DD YYYY hh:mm:ss.SSSSSS A z",
    "dddd, MMMM Do, YYYY hh:mm:ss.SSSSSS A z",
]

ambiguous_datetime = pendulum_datetime(2001, 2, 3, 4, 5, 6, 7)
forgiving_ambiguous_datetime = pendulum_datetime(2001, 1, 1, 1, 1, 1, 1)


def test_unambiguous_formats():
    datetime_str = "Saturday, February 3rd 2001 04:05:06 AM UTC"
    parse_with_formats(datetime_str, formats=unambiguous_formats)


def test_require_unambiguous_formats_with_unambiguous_formats():
    datetime_str = "Saturday, February 3rd 2001 04:05:06 AM UTC"
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    if datetime_config.require_unambiguous_formats:
        parse_with_formats(datetime_str, formats=unambiguous_formats)
    else:
        assert False


def test_empty_formats():
    datetime_str = "02/23/2001 04:05:06 AM"
    parse(datetime_str, formats=empty_formats)


def test_ambiguous_formats_without_enforcement():
    datetime_str = ambiguous_datetime.format(ambiguous_formats[0])
    parse_with_formats(datetime_str, formats=ambiguous_formats)


def test_require_unambiguous_formats_with_ambiguous_formats():
    datetime_str = ambiguous_datetime.format(ambiguous_formats[0])
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    with pytest.raises(AmbiguousDatetimeFormatsError):
        parse_with_formats(
            datetime_str, formats=ambiguous_formats, config=datetime_config
        )


def test_require_unambiguous_formats_with_ambiguous_formats_with_subseconds():
    datetime_str = ambiguous_datetime.format(ambiguous_formats_with_subseconds[0])
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    with pytest.raises(AmbiguousDatetimeFormatsError):
        parse_with_formats(
            datetime_str,
            formats=ambiguous_formats_with_subseconds,
            config=datetime_config,
        )


def test_require_unambiguous_formats_with_ambiguous_formats_with_short_year():
    datetime_str = ambiguous_datetime.format(ambiguous_formats_short_year[0])
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    with pytest.raises(AmbiguousDatetimeFormatsError):
        parse_with_formats(
            datetime_str, formats=ambiguous_formats_short_year, config=datetime_config
        )


def test_forgiving_require_unambiguous_formats_with_ambiguous_formats():
    datetime_str = forgiving_ambiguous_datetime.format(ambiguous_formats[0])
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    parsed_datetime = parse_with_formats(
        datetime_str, formats=ambiguous_formats, config=datetime_config
    )
    assert parsed_datetime._datetime.ctime() == forgiving_ambiguous_datetime.ctime()


def test_forgiving_require_unambiguous_formats_with_ambiguous_formats_with_subseconds():
    datetime_str = forgiving_ambiguous_datetime.format(
        ambiguous_formats_with_subseconds[0]
    )
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    parsed_datetime = parse_with_formats(
        datetime_str,
        formats=ambiguous_formats_with_subseconds,
        config=datetime_config,
    )
    assert parsed_datetime._datetime.ctime() == forgiving_ambiguous_datetime.ctime()


def test_forgiving_require_unambiguous_formats_with_ambiguous_formats_with_short_year():
    datetime_str = forgiving_ambiguous_datetime.format(ambiguous_formats_short_year[0])
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    parsed_datetime = parse_with_formats(
        datetime_str, formats=ambiguous_formats_short_year, config=datetime_config
    )
    assert parsed_datetime._datetime.ctime() == forgiving_ambiguous_datetime.ctime()
