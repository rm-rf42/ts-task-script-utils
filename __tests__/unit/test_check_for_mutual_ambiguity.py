import pytest
from task_script_utils.datetime_parser import DatetimeConfig
from task_script_utils.datetime_parser.utils import check_for_mutual_ambiguity
from task_script_utils.datetime_parser.parser_exceptions import (
    AmbiguousDatetimeFormatsError,
)

ambiguous_formats_list = [
    "MM/DD/YYYY hh:mm:ss A z",
    "DD/MM/YYYY hh:mm:ss A z",
]

unambiguous_formats_list = [
    "dddd, MMMM Do YYYY hh:mm:ss A zz z",
    "dddd, MMMM Do YYYY hh:mm:ss A z",
    "dddd, MMMM Do YYYY hh:mm:ss A zz",
    "dddd, MMMM DD YYYY hh:mm:ss A z",
    "dddd, MMMM Do, YYYY hh:mm:ss A z",
    "dddd, MMMM DD YYYY hh:mm:ss.SSSSSS A z",
    "dddd, MMMM Do, YYYY hh:mm:ss.SSSSSS A z",
]


def test_unambiguous_formats():
    check_for_mutual_ambiguity(formats_list=unambiguous_formats_list)
    assert True


def test_ambiguous_formats():
    with pytest.raises(AmbiguousDatetimeFormatsError):
        check_for_mutual_ambiguity(formats_list=ambiguous_formats_list)


def test_enforcing_unambiguity_with_unambiguous_formats():
    if DatetimeConfig(enforce_unambiguity=True).enforce_unambiguity:
        check_for_mutual_ambiguity(formats_list=unambiguous_formats_list)
        assert True
    else:
        assert False


def test_enforcing_unambiguity_with_ambiguous_formats():
    if DatetimeConfig(enforce_unambiguity=True).enforce_unambiguity:
        with pytest.raises(AmbiguousDatetimeFormatsError):
            check_for_mutual_ambiguity(formats_list=ambiguous_formats_list)
    else:
        assert False
