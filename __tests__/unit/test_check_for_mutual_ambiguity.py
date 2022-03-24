import pytest
from task_script_utils.datetime_parser import DatetimeConfig
from task_script_utils.datetime_parser.utils.checks import check_for_mutual_ambiguity
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


def test_unambiguous_formats():
    check_for_mutual_ambiguity(formats=unambiguous_formats)


def test_empty_formats():
    check_for_mutual_ambiguity(formats=empty_formats)


def test_ambiguous_formats():
    with pytest.raises(AmbiguousDatetimeFormatsError):
        check_for_mutual_ambiguity(formats=ambiguous_formats)


def test_enforcing_unambiguity_with_unambiguous_formats():
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    if datetime_config.require_unambiguous_formats:
        check_for_mutual_ambiguity(formats=unambiguous_formats)
    else:
        assert False


def test_enforcing_unambiguity_with_ambiguous_formats():
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    if datetime_config.require_unambiguous_formats:
        with pytest.raises(AmbiguousDatetimeFormatsError):
            check_for_mutual_ambiguity(formats=ambiguous_formats)
    else:
        assert False


def test_enforcing_unambiguity_with_ambiguous_formats_with_subseconds():
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    if datetime_config.require_unambiguous_formats:
        with pytest.raises(AmbiguousDatetimeFormatsError):
            check_for_mutual_ambiguity(formats=ambiguous_formats_with_subseconds)
    else:
        assert False


def test_enforcing_unambiguity_with_ambiguous_formats_with_short_year():
    datetime_config = DatetimeConfig(require_unambiguous_formats=True)
    if datetime_config.require_unambiguous_formats:
        with pytest.raises(AmbiguousDatetimeFormatsError):
            check_for_mutual_ambiguity(formats=ambiguous_formats_short_year)
    else:
        assert False
