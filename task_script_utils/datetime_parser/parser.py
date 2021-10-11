import pendulum
from dateutil.parser import parse as dateutil_parse
from .pipeline_config import PipelineConfig
from .datetime_info import DateTimeInfo

def parse(
    datetime_str: str,
    formats_list: list = None,
    config: PipelineConfig = PipelineConfig.from_dict({})
):
    parsed_datetime = None

    # Parse Using formats list
    if formats_list:
        parsed_datetime, matched_format = parse_with_formats(
            datetime_str, formats_list)
        if parsed_datetime:
            return parsed_datetime

    # Parse Using dateutil.parser.parse
    parsed_datetime = parse_using_dateutils(datetime_str, config)
    if parsed_datetime:
        return parsed_datetime

    # Otherwise use DateInfo Parser to parse short dates
    try:
        dt_info = DateTimeInfo(datetime_str, config)
        parsed_datetime = dt_info.datetime_object
    except Exception as e:
        raise(e)

    # TODO: parse long datetime formats
    return parsed_datetime


def parse_with_formats(datetime_str: str, formats: list = None):
    for format in formats:
        try:
            parsed = pendulum.from_format(datetime_str, format)
            return parsed, format
        except Exception as e:
            continue
    return None, None

def parse_using_dateutils(datetime_str: str, config:PipelineConfig):
    try:
        parsed_datetime = dateutil_parse(
            datetime_str,
            dayfirst=config.day_first,
            yearfirst=config.year_first,
        )
        return parsed_datetime
    except Exception as e:
        return None