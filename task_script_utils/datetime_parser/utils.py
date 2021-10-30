import datetime as dt
from typing import List

from pendulum.formatting import formatter


def convert_offset_to_seconds(offset_value):
    """Convert +/-hh:mm utc offset string value
    to +/-<seconds>
    eg. +00:33 --> 1980.0
    eg. -00:33 --> -1980.0
    """
    sign, offset = offset_value[0], offset_value[1:]
    sign = -1 if sign == "-" else 1
    hrs, mins = offset.split(":")
    total_seconds = dt.timedelta(
        hours=int(hrs),
        minutes=int(mins)
    ).total_seconds()
    return sign * total_seconds


def map_offset_to_seconds(tz_dict):
    """
    Convert dict that maps from abbreviated_tz -> utc_offset
    to a dict that maps abbreviated_tz -> total_seconds
    eg. {"ist": "+05:30"} ---> {"ist": 19800.0}
    """
    return {
        tz.upper(): convert_offset_to_seconds(utc_offset)
        for tz, utc_offset
        in tz_dict.items()
    }


def replace_abbreviated_tz_with_utc_offset(datetime_str: str, tz_dict):
    """
    Converts `12-12-2012 12:12:12 AM IST` to `12-12-2012 12:12:12 AM +05:30`
    if `IST: +05:30` exist in tz_dict
    """
    for tz in tz_dict:
        if tz in datetime_str:
            return datetime_str.replace(tz, tz_dict[tz])
    return datetime_str


def replace_zz_with_Z(formats: List[str]):
    """
    eg. `DD-MM-YYYY hh:m:ss zz` -> `DD-MM-YYYY hh:m:ss Z`
    """
    result_formats = list(formats)
    for idx, format_ in enumerate(result_formats):
        if " zz" in format_:
            result_formats[idx] = format_.replace(" zz", " Z")

    return result_formats