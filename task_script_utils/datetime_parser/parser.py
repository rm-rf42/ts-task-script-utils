from datetime import datetime
from typing import List
import pendulum
from pendulum.datetime import DateTime as PendulumDateTime
from pendulum.tz.timezone import Timezone
from dateutil import tz
from dateutil.parser import parse as dateutil_parse

from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError
from .pipeline_config import PipelineConfig
from .datetime_info import DateTimeInfo
from .date_formats import get_long_datetime_formats
from .utils import (
    convert_offset_to_seconds,
    replace_abbreviated_tz_with_utc_offset,
    replace_zz_with_Z
)


DEFAULT_PIPELINE_CONFIG = PipelineConfig()


def parse(
    datetime_str: str,
    formats_list: List[str] = [],
    config: PipelineConfig = DEFAULT_PIPELINE_CONFIG
):
    parsed_datetime = None

    # Parse Using formats list
    if formats_list:
        parsed_datetime, matched_format = parse_with_formats(
            datetime_str,
            pipeline_config=config,
            formats=formats_list
        )
        if parsed_datetime:
            parsed_datetime = change_fold(parsed_datetime, config.fold)
            return parsed_datetime

    # Parse Using dateutil.parser.parse
    parsed_datetime = parse_using_dateutils(datetime_str, config)
    if parsed_datetime:
        parsed_datetime = change_fold(parsed_datetime, config.fold)
        return parsed_datetime

    # Otherwise use DateInfo Parser to parse short dates
    dt_info = DateTimeInfo(datetime_str, config)
    dt_info.parse()
    if dt_info.dtstamp:
        parsed_datetime = dt_info.datetime
        parsed_datetime = change_fold(parsed_datetime, config.fold)
        return parsed_datetime

    # Use long date formats
    if not parsed_datetime:
        parsed_datetime, _ = parse_with_formats(
            datetime_str=datetime_str,
            formats=get_long_datetime_formats(),
            pipeline_config=config

        )

    if parsed_datetime is None:
        raise DatetimeParserError(f"Could no parse: {datetime_str}")

    parsed_datetime = change_fold(parsed_datetime, config.fold)
    return parsed_datetime


def parse_with_formats(
    datetime_str: str,
    pipeline_config: PipelineConfig,
    formats: list = []
):
    # If pipeline config contains tz_dict, then replace
    # abbreviated_tz in datetime_str with its corresponding
    # utc offset values from pipeline_config.tz_dict
    datetime_str_with_no_abbreviated_tz = replace_abbreviated_tz_with_utc_offset(
        datetime_str,
        pipeline_config.tz_dict
    )
    if datetime_str_with_no_abbreviated_tz != datetime_str:
        # It means datetime_str did contain abbreviated_tz and we
        # have replaced it with its utc_offset value from tz_dict.
        # Now if the format in formats_list contains "zz", replace
        # it with "Z". This is because no library parses abbreviated tz
        # due to its ambiguous nature
        formats_with_no_zz = replace_zz_with_Z(formats)
    else:
        formats_with_no_zz = formats

    for format_ in formats_with_no_zz:
        try:
            parsed = pendulum.from_format(
                datetime_str_with_no_abbreviated_tz,
                format_
            )
            return parsed, format_
        except Exception as e:
            continue
    return None, None


def parse_using_dateutils(datetime_str: str, config: PipelineConfig):
    try:
        if (
            (config.day_first is not None)
            and (config.year_first is not None)
        ):
            parsed_datetime = dateutil_parse(
                datetime_str,
                dayfirst=config.day_first,
                yearfirst=config.year_first,
                tzinfos=config.tz_dict
            )
            return parsed_datetime
    except Exception as e:
        return None


def change_time_zone(parsed_datetime, datetime_str, config: PipelineConfig):
    tz_ = None
    offset = None
    config_timezones = config.tz_dict
    for timezone, potential_offset in config_timezones.items():
        if timezone.lower() in datetime_str.lower():
            tz_ = timezone
            offset = potential_offset
            break

    if offset is None:
        return parsed_datetime

    offset_seconds = convert_offset_to_seconds(offset)
    tz_local = tz.tzoffset(tz_, offset_seconds)
    local_parsed_time = parsed_datetime.replace(tzinfo=tz_local)
    return local_parsed_time


def change_fold(dt_obj: PendulumDateTime, config_fold: int):
    if (
        dt_obj.tzinfo is None
        or config_fold is None
        or config_fold == dt_obj.fold
    ):
        return dt_obj

    new_dt_obj: PendulumDateTime = dt_obj.replace(fold=config_fold)
    return new_dt_obj