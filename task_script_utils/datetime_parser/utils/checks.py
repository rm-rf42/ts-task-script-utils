from itertools import combinations
from typing import Sequence

from pendulum import datetime as pendulum_datetime
from task_script_utils.datetime_parser.datetime_config import (
    DEFAULT_DATETIME_CONFIG,
    DatetimeConfig,
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
    formats: Sequence[str] = (),
):
    """Checks if any of the datetime formats in `formats` are mutually ambiguous.

    Args:
        datetime_config (DatetimeConfig, optional): A python dict that maps abbreviated
        timezone names to their corresponding offset. Defaults to
        DEFAULT_DATETIME_CONFIG
        formats (Sequence[str], optional): List of possible datetime formats.
        Defaults to empty tuple.

    Raises:
        AmbiguousDatetimeFormatsError: Exception to be raised if any of the datetime
        formats are found to be mutually ambiguous.
    """
    tz_dict = datetime_config.tz_dict
    formats = replace_zz_with_Z(formats)
    ambiguous_datetime = pendulum_datetime(2001, 2, 3, 4, 5, 6, 7)
    sample_datetimes = [
        replace_abbreviated_tz_with_utc_offset(
            ambiguous_datetime.format(format_), tz_dict
        )
        for format_ in formats
    ]

    for (sample_datetime, datetime_format_1), (_, datetime_format_2) in combinations(
        zip(sample_datetimes, formats), 2
    ):
        try:
            ambiguous_datetime_format_1 = from_pendulum_format(
                sample_datetime, datetime_format_1, tz=None
            )
            ambiguous_datetime_format_2 = from_pendulum_format(
                sample_datetime, datetime_format_2, tz=None
            )
            if (
                ambiguous_datetime_format_1.tsformat()
                != ambiguous_datetime_format_2.tsformat()
            ):
                raise AmbiguousDatetimeFormatsError(
                    f"Ambiguity found between datetime formats [{datetime_format_1}]"
                    f" and [{datetime_format_2}]. Formats parsed [{ambiguous_datetime}]"
                    f" to [{ambiguous_datetime_format_1.tsformat()}] and"
                    f" [{ambiguous_datetime_format_2.tsformat()}], respectively."
                )
        except ValueError:
            # Ignoring ValueError because we're not concerned
            # about validity of parses in this function
            pass
