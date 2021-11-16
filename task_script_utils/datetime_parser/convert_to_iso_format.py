from datetime import date
from typing import Optional, Tuple

import pendulum

from task_script_utils.datetime_parser.datetime_info import DateTimeInfo

from .datetime_config import DatetimeConfig, DEFAULT_DATETIME_CONFIG
from .parser import parse


def convert_to_ts_iso8601(
    datetime_str: str,
    formats_list: Tuple[str] = (),
    config: DatetimeConfig = DEFAULT_DATETIME_CONFIG
):
    """Convert datetime_str to ISO8601 format, if datetime_str
    is valid and parse-able.

    Args:
        datetime_str (str): raw datetime string
        formats_list (List[str], optional): List of possible datetime formats.
        These datetime formats must be built using `pendulum` datetime tokens.
        Defaults to [].
        config (DatetimeConfig, optional): Datetime Configuration.
        Defaults to DatetimeCoonfig().

    Returns:
        [type]: IS08601 datetime string
    """
    parsed_datetime, datetime_info, matched_format = parse(
        datetime_str=datetime_str,
        formats_list=formats_list,
        config=config
    )

    ts_format = _build_ts_format(datetime_info)

    if parsed_datetime.tzinfo is not None:
        utc = pendulum.tz.UTC
        parsed_datetime = utc.convert(parsed_datetime)
        iso_8601 = parsed_datetime.format(ts_format) + "Z"
    else:
        iso_8601 = parsed_datetime.format(ts_format)

    return iso_8601


def _build_ts_format(datetime_info: Optional[DateTimeInfo]):
    default_format = "YYYY-MM-DDTHH:mm:ss"

    if datetime_info is None:
        return f"{default_format}.SSS"

    if datetime_info.fractional_seconds is None:
        return f"{default_format}.SSS"

    subseconds = datetime_info.fractional_seconds
    subseconds_token = "S"* len(subseconds)

    return f"{default_format}.{subseconds_token}"