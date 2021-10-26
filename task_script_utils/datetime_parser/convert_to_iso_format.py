from typing import List

import pendulum
from pendulum.datetime import DateTime as PendulumDateTime

from .pipeline_config import PipelineConfig
from .parser import parse


def convert_to_iso8601(
    datetime_str: str,
    formats_list: List[str] = None,
    config: PipelineConfig = PipelineConfig(),
):
    parsed_datetime = parse(
        datetime_str=datetime_str,
        formats_list=formats_list,
        config=config
    )

    if parsed_datetime.tzinfo is not None:
        utc = pendulum.tz.UTC
        parsed_datetime = utc.convert(parsed_datetime)
        iso_8601 = _get_iso8601(parsed_datetime) + "Z"
    else:
        iso_8601 = _get_iso8601(parsed_datetime)

    return iso_8601


def _get_iso8601(datetime: PendulumDateTime):
    fmt = "YYYY-MM-DDTHH:mm:ss"
    if datetime.microsecond:
        fmt += ".SSS"

    return datetime.format(fmt)
