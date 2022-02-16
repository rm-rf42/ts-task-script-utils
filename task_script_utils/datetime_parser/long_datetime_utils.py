from typing import Tuple
from itertools import product

from pydash.arrays import flatten

from .parser_exceptions import InvalidDateError
from .datetime_info import DateTimeInfo

TIME_PARTS = [
    ["h", "hh", "H", "HH"],
    ["m", "mm"],
    ["s", "ss"],
]


def get_time_formats_for_long_date(fractional_seconds):
    def map_am_pm(time_format):
        return time_format if time_format.startswith("H") else time_format + " A"

    time_formats = [":".join(tokens) for tokens in product(*TIME_PARTS)]
    if fractional_seconds:
        token = "SSSSSS"
        time_formats = map(lambda x: [x, f"{x}.{token}"], time_formats)

    time_formats = flatten(time_formats)
    time_formats = map(lambda x: map_am_pm(x), time_formats)
    time_formats = map(
        lambda x: [x, x + " Z", x + " z", x + " ZZ", x + " Z z", x + " ZZ z"],
        time_formats,
    )
    time_formats = flatten(time_formats)
    return tuple(time_formats)


def build_long_date_format_from_datetime_info(dt_info:DateTimeInfo):
    """Use DatetimeInfo to build and return date format for
    log datetime string.

    Raises:
        InvalidDateError: Raised if parsing fails to
        detect tokens for month or day

    Returns:
        str: Return Date format built using pendulum
        formatting tokens
    """
    if not (dt_info.token_month and dt_info.token_day):
        raise InvalidDateError(f"{dt_info.date_time_raw}")

    if dt_info.token_day_of_week:
        date_fmt = (
            f"{dt_info.token_day_of_week} "
            f"{dt_info.token_month} "
            f"{dt_info.token_day} "
            f"YYYY"
        )
    else:
        date_fmt = f"{dt_info.token_month} {dt_info.token_day} YYYY"
    return date_fmt


def build_long_datetime_formats_list(dt_info: DateTimeInfo) -> Tuple[str]:
    """Returns a list of long datetime formats built
    using pendulum formatting tokens.
    """
    parts = [
        [build_long_date_format_from_datetime_info(dt_info)],
        get_time_formats_for_long_date(dt_info.fractional_seconds),
    ]
    formats = tuple(" ".join(values) for values in product(*parts))
    return formats
