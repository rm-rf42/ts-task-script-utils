from typing import Sequence

import pendulum

from .datetime_config import DatetimeConfig, DEFAULT_DATETIME_CONFIG
from .parser import parse


def convert_to_ts_iso8601(
    datetime_raw_str: str,
    formats_list: Sequence[str] = (),
    config: DatetimeConfig = DEFAULT_DATETIME_CONFIG,
) -> str:
    """Convert datetime_str to ISO8601 format, if datetime_str
    is valid and parse-able.

    Args:
        datetime_str (str): raw datetime string
        formats_list (Sequence[str], optional): List of possible datetime formats.
        These datetime formats must be built using `pendulum` datetime tokens.
        Defaults to [].
        config (DatetimeConfig, optional): Datetime Configuration.
        Defaults to DatetimeConfig().

    Returns:
        str: IS08691 datetime string
    """
    parsed_datetime = parse(
        datetime_raw_str=datetime_raw_str, formats_list=formats_list, config=config
    )
    return parsed_datetime.tsformat()
