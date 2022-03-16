import datetime as dt
import re
from itertools import product
from typing import Dict, Optional, Sequence

from pendulum import datetime as pendulum_datetime
from pendulum import now
from pydash.arrays import flatten

from .fractional_seconds_formatter import FractionalSecondsFormatter
from .parser_exceptions import AmbiguousDatetimeFormatsError
from .ts_datetime import TSDatetime

_formatter = FractionalSecondsFormatter()

TIME_PARTS = [
    ["h", "hh", "H", "HH"],
    ["m", "mm"],
    ["s", "ss"],
]


def get_time_formats_for_long_date(fractional_seconds: Optional[str]):
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


def convert_offset_to_seconds(offset_value: str):
    """Convert +/-hh:mm utc offset string value
    to +/-<seconds>
    eg. +00:33 --> 1980.0
    eg. -00:33 --> -1980.0
    """
    sign, offset = offset_value[0], offset_value[1:]
    sign = -1 if sign == "-" else 1
    hrs, mins = offset.split(":")
    total_seconds = dt.timedelta(hours=int(hrs), minutes=int(mins)).total_seconds()
    return sign * total_seconds


def map_offset_to_seconds(tz_dict):
    """
    Convert dict that maps from abbreviated_tz -> utc_offset
    to a dict that maps abbreviated_tz -> total_seconds
    eg. {"ist": "+05:30"} ---> {"ist": 19800.0}
    """
    return {
        tz.upper(): convert_offset_to_seconds(utc_offset)
        for tz, utc_offset in tz_dict.items()
    }


def replace_abbreviated_tz_with_utc_offset(
    datetime_str: str, tz_dict: Optional[Dict] = {}
):
    """
    Converts `12-12-2012 12:12:12 AM IST` to `12-12-2012 12:12:12 AM +05:30`
    if `IST: +05:30` exist in tz_dict
    """
    for tz in tz_dict:
        if tz in datetime_str:
            return datetime_str.replace(tz, tz_dict[tz])
    return datetime_str


def replace_zz_with_Z(formats: Optional[Sequence[str]] = ()):
    """
    eg. `DD-MM-YYYY hh:m:ss zz` -> `DD-MM-YYYY hh:m:ss Z`
    """
    result_formats = list(formats)
    for idx, format_ in enumerate(result_formats):
        if " zz" in format_:
            result_formats[idx] = format_.replace(" zz", " Z")

    return result_formats


def from_pendulum_format(
    datetime_string: str,
    fmt: str,
    tz=None,
    locale=None,
) -> TSDatetime:
    """
    Creates a DateTime instance from a specific format.
    """
    subseconds = None
    parts = _formatter.parse(datetime_string, fmt, now(), locale=locale)
    if parts["tz"] is None:
        parts["tz"] = tz

    if "S" in fmt:
        subseconds = parts["microsecond"]
        parts["microsecond"] = 0

    ts_date_time = TSDatetime(
        datetime_=pendulum_datetime(**parts), subseconds=subseconds
    )
    return ts_date_time


def replace_z_with_offset(datetime_str: str) -> str:
    """
    12-12-12T14:53:00Z -> 12-12-12T14:53:00+00:00
    12-12-12T14:53:00 Z -> 12-12-12T14:53:00 +00:00
    """
    return re.sub(r"(?<=\d|\s)Z(?=\s|$)", "+00:00", datetime_str)


def check_for_mutual_ambiguity(
    tz_dict: Optional[Dict] = {},
    formats_list: Optional[Sequence[str]] = (),
):
    """Checks if any of the datetime formates in `formats_list` are mutually ambiguous.

    Args:
        tz_dict (Optional[Dict], optional): A python dict that maps abbreviated timezone
        names to their corresponding offset. Defaults to {}.
        formats_list (Optional[Sequence[str]], optional): List of possible datetime
        formats. Defaults to ().

    Raises:
        AmbiguousDatetimeFormatsError: Exception to be raised if any of the datetime
        formats are found to be mutually ambiguous.
    """
    formats_list = replace_zz_with_Z(formats_list)
    ambiguous_datetime = pendulum_datetime(2001, 2, 3, 4, 5, 6, 7)
    formats_list = set(formats_list)
    for datetime_format in formats_list:
        input_ = ambiguous_datetime.format(datetime_format)
        for other_datetime_format in formats_list - {datetime_format}:
            try:
                utc_offset_datatime = replace_abbreviated_tz_with_utc_offset(
                    input_, tz_dict
                )
                input_ = (
                    replace_zz_with_Z(utc_offset_datatime)
                    if utc_offset_datatime != input_
                    else input_
                )

                ambiguous_format_datetime = from_pendulum_format(
                    input_, datetime_format, tz=tz_dict
                )
                other_ambiguous_format_datetime = from_pendulum_format(
                    input_, other_datetime_format, tz=tz_dict
                )
                print(ambiguous_format_datetime, other_ambiguous_format_datetime)
                if input_ != other_ambiguous_format_datetime:
                    raise AmbiguousDatetimeFormatsError(
                        f"""
                        Ambiguity found between datetime formats [{datetime_format}] and
                        [{other_datetime_format}]. Formats parsed [{ambiguous_datetime}]
                        to [{ambiguous_format_datetime}] and
                        [{other_ambiguous_format_datetime}], respectively.
                        """
                    )
            except ValueError:
                # Ignoring ValueError because we're not concerned about validity of
                # parses in this function
                pass
            except AssertionError:
                # Ignoring AssertionErrors because we're not concerned about
                # validity of parses in this function
                pass
