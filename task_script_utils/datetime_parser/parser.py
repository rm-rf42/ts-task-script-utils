<<<<<<< HEAD
from re import sub
from typing import Tuple
=======
from typing import Sequence, Tuple
>>>>>>> DE-2591-datetime-parser
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
    from_pendulum_format
)


def parse(
    datetime_str: str,
    formats_list: Sequence[str] = (),
    config: DatetimeConfig = DEFAULT_DATETIME_CONFIG
) -> TSDatetime:
    parsed_datetime = None
    datetime_info = None


    # Parse Using formats list
    if formats_list:
        parsed_datetime, matched_format = _parse_with_formats(
            datetime_str,
            datetime_config=config,
            formats=formats_list
        )

    # Parse Using dateutil.parser.parse
    if not parsed_datetime:
        parsed_datetime = _parse_using_dateutils(datetime_str, config)

    # Otherwise use DateInfo Parser to parse short dates
    if not parsed_datetime:
        datetime_info = DateTimeInfo(datetime_str, config)
        if datetime_info.dtstamp:
            parsed_datetime = TSDatetime(
                datetime_=datetime_info.datetime,
                subseconds=datetime_info.fractional_seconds
            )

    # Use long date formats
    if not parsed_datetime:
        parsed_datetime, matched_format = _parse_with_formats(
            datetime_str=datetime_str,
            formats=datetime_info.long_datetime_formats,
            datetime_config=config

        )

    if parsed_datetime is None:
        raise DatetimeParserError(f"Could not parse: {datetime_str}")

    if not isinstance(parsed_datetime, TSDatetime):
        parsed_datetime = TSDatetime(datetime_=parsed_datetime)

    parsed_datetime.change_fold(config.fold)
    return parsed_datetime


def _parse_with_formats(
    datetime_str: str,
    datetime_config: DatetimeConfig,
    formats: Sequence[str] = ()
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
            parsed = from_pendulum_format(
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