from itertools import combinations
from typing import Optional, Sequence
from pendulum import datetime as pendulum_datetime
from task_script_utils.datetime_parser.datetime_config import (
    DatetimeConfig,
    DEFAULT_DATETIME_CONFIG,
)
from task_script_utils.datetime_parser.parser_exceptions import (
    AmbiguousDatetimeFormatsError,
)
from task_script_utils.datetime_parser.utils.conversions import (
    from_pendulum_format,
    replace_abbreviated_tz_with_utc_offset,
    replace_zz_with_Z,
)


def check_for_mutual_ambiguity(
    datetime_config: DatetimeConfig = DEFAULT_DATETIME_CONFIG,
    formats_list: Sequence[str] = (),
):
    """Checks if any of the datetime formats in `formats_list` are mutually ambiguous.

    Args:
        tz_dict (DatetimeConfig, optional): A python dict that maps abbreviated timezone
        names to their corresponding offset. Defaults to DEFAULT_DATETIME_CONFIG.
        formats_list (Sequence[str], optional): List of possible datetime formats.
        Defaults to ().

    Raises:
        AmbiguousDatetimeFormatsError: Exception to be raised if any of the datetime
        formats are found to be mutually ambiguous.
    """
    tz_dict = datetime_config.tz_dict
    formats_list = replace_zz_with_Z(formats_list)
    ambiguous_datetime = pendulum_datetime(2001, 2, 3, 4, 5, 6, 7)

    for datetime_format_1, datetime_format_2 in combinations(formats_list, 2):
        input_ = ambiguous_datetime.format(datetime_format_1)
        try:
            utc_offset_datatime = replace_abbreviated_tz_with_utc_offset(
                input_, tz_dict
            )
            input_ = (
                replace_zz_with_Z(utc_offset_datatime)
                if utc_offset_datatime != input_
                else input_
            )

            ambiguous_datetime_format_1 = from_pendulum_format(
                input_, datetime_format_1, tz=None
            )
            other_ambiguous_datetime_format_2 = from_pendulum_format(
                input_, datetime_format_2, tz=None
            )
            if input_ != other_ambiguous_datetime_format_2:
                raise AmbiguousDatetimeFormatsError(
                    f"""
                    Ambiguity found between datetime formats [{datetime_format_1}] and
                    [{datetime_format_2}]. Formats parsed [{ambiguous_datetime}]
                    to [{ambiguous_datetime_format_1.tsformat()}] and
                    [{other_ambiguous_datetime_format_2.tsformat()}], respectively.
                    """
                )
        except (ValueError, AssertionError):
            # Ignoring ValueError and AssertionErrors because we're not concerned
            # about validity of parses in this function
            pass
