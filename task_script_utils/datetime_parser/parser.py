import datetime as dt
import pendulum
from dateutil import tz
from dateutil.parser import parse as dateutil_parse
from .pipeline_config import PipelineConfig
from .datetime_info import DateTimeInfo
from .date_formats import get_long_datetime_formats
from .utils import convert_offset_to_seconds
default_pipline_config = PipelineConfig.from_dict({})


def parse(
    datetime_str: str,
    formats_list: list = None,
    config: PipelineConfig = default_pipline_config
):
    parsed_datetime = None

    # Parse Using formats list
    if formats_list:
        parsed_datetime, matched_format = parse_with_formats(
            datetime_str,
            formats_list
        )
        if parsed_datetime:
            if config.tz_dict:
                parsed_datetime = change_time_zone(
                    parsed_datetime,
                    datetime_str,
                    config
                )
            return parsed_datetime

    # Parse Using dateutil.parser.parse
    parsed_datetime = parse_using_dateutils(datetime_str, config)
    if parsed_datetime:
        return parsed_datetime

    # Otherwise use DateInfo Parser to parse short dates
    dt_info = DateTimeInfo(datetime_str, config)
    dt_info.parse()
    if dt_info.dtstamp:
        parsed_datetime = dt_info.datetime

    # Use long date formats
    if not parsed_datetime:
        parsed_datetime = parse_with_formats(
            datetime_str,
            get_long_datetime_formats()
        )
    return parsed_datetime


def parse_with_formats(datetime_str: str, formats: list = None):
    for format in formats:
        try:
            parsed = pendulum.from_format(datetime_str, format, tz=None)
            return parsed, format
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
