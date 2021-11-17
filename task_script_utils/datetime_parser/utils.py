import re
import datetime as dt
from typing import List
from itertools import product

from pydash.arrays import flatten

from task_script_utils.datetime_parser.patterns import (
    token_to_regex,
    token_to_name,
    tokens_regex
)

TOKEN_NAMES = {
    'Y': "year",
    'YY': "year",
    'YYYY': "year",

    'Q': "quarter",
    'Qo': "quarter",

    'M': "month",
    'MM': "month",
    'MMM': "month",
    'MMMM': "month",

    'D': "day_of_month",
    'DD': "day_of_month",
    'Do': "day_of_month",

    'DDD': "day_of_year",
    'DDDD': "day_of_year",

    'dddd': "day_of_week",
    'ddd': "day_of_week",
    'dd':  "day_of_week",
    'd': "day_of_week",
    'E': "day_of_week",

    'H': "hour",
    'HH': "hour",
    'h': "hour",
    'hh': "hour",

    'm': "minutes",
    'mm': "minutes",
    's': "seconds",
    'ss': "seconds",

    'x': "milliseconds_ts",
    'X': "seconds_ts",
    'ZZ': "tz",
    'Z': "tz",
    'z': "tz",
    'A': "am_pm"
}

TIME_PARTS = [
    ["h", "hh", "H", "HH"],
    ["m", "mm"],
    ["s", "ss"],
]

def get_time_formats_for_long_date(fractional_seconds):
    def map_am_pm(time_format):
        return (
            time_format
            if time_format.startswith("H")
            else time_format + " A"
        )

    time_formats = [
        ":".join(tokens)
        for tokens in product(*TIME_PARTS)
    ]
    if fractional_seconds:
        token = "S" * len(fractional_seconds)
        time_formats = map(lambda x: [x, f"{x}.{token}"], time_formats)

    time_formats = flatten(time_formats)
    time_formats = map(lambda x: map_am_pm(x), time_formats)
    time_formats = map(
        lambda x: [
            x,
            x + " Z",
            x + " z",
            x + " ZZ",
            x + " Z z",
            x + " ZZ z"],
        time_formats
    )
    time_formats = flatten(time_formats)
    return tuple(time_formats)


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


def get_subseconds(raw_datetime_string, matched_format):
    format_ = [re.escape(token) for token in matched_format.split(" ")]

    for idx, part in enumerate(format_):
        # Get tokens present in he format part
        tokens = tokens_regex.findall(part)
        tokens = map(lambda x: [token for token in x if token], tokens)
        tokens = map(lambda x: x[0], tokens)
        tokens = filter(lambda x: x.isalpha() and "S" not in x, tokens)

        # map tokens to their corresponding regex
        tokens = {token: token_to_regex[token] for token in tokens}

        # for each token in the part
        # replace it with its corresponding pattern
        for token, regex in tokens.items():
            candidates = regex
            if not isinstance(candidates, tuple):
                candidates = (candidates, )

            pattern = "(?P<{}>{})".format(
                token_to_name[token], "|".join([p for p in candidates]))
            format_[idx] = format_[idx].replace(token, pattern)
        if "S" in part:
            num_S = part.count("S")
            subsecond_token = num_S * "S"
            format_[idx] = format_[idx].replace(
                subsecond_token, r'(?P<subsecond>\d+)')

    re_format = " ".join(format_)
    match = re.fullmatch(re_format,raw_datetime_string)
    return match.group('subsecond')

