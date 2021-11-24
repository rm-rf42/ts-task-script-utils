from typing import Sequence

import pendulum

from .datetime_config import DatetimeConfig, DEFAULT_DATETIME_CONFIG
from .parser import parse


def convert_to_ts_iso8601(
    datetime_str: str,
    formats_list: Sequence[str] = (),
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
        [type]: IS08691 datetime string
    """
    ts_format = "YYYY-MM-DDTHH:mm:ss.SSS"
    parsed_datetime = parse(
        datetime_str=datetime_str,
        formats_list=formats_list,
        config=config
    )

    if parsed_datetime.tzinfo is not None:
        utc = pendulum.tz.UTC
        parsed_datetime = utc.convert(parsed_datetime)
        iso_8601 = parsed_datetime.format(ts_format) + "Z"
    else:
        iso_8601 = parsed_datetime.format(ts_format)

    return iso_8601