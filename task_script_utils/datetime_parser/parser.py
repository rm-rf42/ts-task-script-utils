from re import sub
from typing import Tuple
import pendulum
from pendulum.datetime import DateTime as PendulumDateTime
from dateutil.parser import parse as dateutil_parse

from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError
from task_script_utils.datetime_parser.ts_datetime import TSDatetime
from .datetime_config import DatetimeConfig, DEFAULT_DATETIME_CONFIG
from .datetime_info import DateTimeInfo
from .utils import (
    replace_abbreviated_tz_with_utc_offset,
    replace_zz_with_Z,
    get_subseconds
)


def parse(
    datetime_str: str,
    formats_list: Tuple[str] = (),
    config: DatetimeConfig = DEFAULT_DATETIME_CONFIG
):
    parsed_datetime = None
    datetime_info = None
    matched_format = None
    subseconds = None

    # Parse Using formats list
    if formats_list:
        parsed_datetime, matched_format = _parse_with_formats(
            datetime_str,
            datetime_config=config,
            formats=formats_list
        )
        if matched_format and "S" in matched_format:
            subseconds = get_subseconds(datetime_str, matched_format)

    # Parse Using dateutil.parser.parse
    if not parsed_datetime:
        parsed_datetime = _parse_using_dateutils(datetime_str, config)

    # Otherwise use DateInfo Parser to parse short dates
    if not parsed_datetime:
        datetime_info = DateTimeInfo(datetime_str, config)
        if datetime_info.dtstamp:
            parsed_datetime = datetime_info.datetime
            subseconds = datetime_info.fractional_seconds

    # Use long date formats
    if not parsed_datetime:
        parsed_datetime, matched_format = _parse_with_formats(
            datetime_str=datetime_str,
            formats=datetime_info.long_datetime_formats,
            datetime_config=config

        )
        if matched_format and "S" in matched_format:
            subseconds = get_subseconds(datetime_str, matched_format)

    if parsed_datetime is None:
        raise DatetimeParserError(f"Could not parse: {datetime_str}")

    parsed_datetime = _change_fold(parsed_datetime, config.fold)
    parsed_datetime = TSDatetime(parsed_datetime, subseconds)

    return parsed_datetime, datetime_info, matched_format


def _parse_with_formats(
    datetime_str: str,
    datetime_config: DatetimeConfig,
    formats: Tuple = ()
):
    # If datetime config contains tz_dict, then replace
    # abbreviated_tz in datetime_str with its corresponding
    # utc offset values from datetime_config.tz_dict
    datetime_str_with_no_abbreviated_tz = replace_abbreviated_tz_with_utc_offset(
        datetime_str,
        datetime_config.tz_dict
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
                format_,
                tz=None
            )
            return parsed, format_
        except Exception as e:
            continue
    return None, None


def _parse_using_dateutils(datetime_str: str, config: DatetimeConfig):
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


def _change_fold(dt_obj: PendulumDateTime, config_fold: int):
    if (
        dt_obj.tzinfo is None
        or config_fold is None
        or config_fold == dt_obj.fold
    ):
        return dt_obj

    new_dt_obj: PendulumDateTime = dt_obj.replace(fold=config_fold)
    return new_dt_obj
