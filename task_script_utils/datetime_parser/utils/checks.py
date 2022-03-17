from typing import Optional, Sequence
from pendulum import datetime as pendulum_datetime
from task_script_utils.datetime_parser.datetime_config import DatetimeConfig
from task_script_utils.datetime_parser.parser_exceptions import (
    AmbiguousDatetimeFormatsError,
)
from task_script_utils.datetime_parser.utils.conversions import (
    from_pendulum_format,
    replace_abbreviated_tz_with_utc_offset,
    replace_zz_with_Z,
)


def check_for_mutual_ambiguity(
    datetime_config: Optional[DatetimeConfig] = DatetimeConfig(),
    formats_list: Optional[Sequence[str]] = (),
):
    """Checks if any of the datetime formats in `formats_list` are mutually ambiguous.

    Args:
        tz_dict (Optional[DatetimeConfig], optional): A python dict that maps
        abbreviated timezone names to their corresponding offset. Defaults to
        DEFAULT_DATETIME_CONFIG. formats_list (Optional[Sequence[str]], optional): List
        of possible datetime formats. Defaults to ().

    Raises:
        AmbiguousDatetimeFormatsError: Exception to be raised if any of the datetime
        formats are found to be mutually ambiguous.
    """
    tz_dict = datetime_config.tz_dict
    formats_list = replace_zz_with_Z(formats_list)
    ambiguous_datetime = pendulum_datetime(2001, 2, 3, 4, 5, 6, 7)
    for idx, datetime_format in enumerate(formats_list):
        input_ = ambiguous_datetime.format(datetime_format)
        if idx - len(formats_list) == 1:
            break
        for other_datetime_format in formats_list[idx + 1 :]:
            try:
                utc_offset_datatime = replace_abbreviated_tz_with_utc_offset(
                    input_, tz_dict
                )
                input_ = (
                    replace_zz_with_Z(utc_offset_datatime)
                    if utc_offset_datatime != input_
                    else input_
                )

                ambiguous_format_datetime = from_pendulum_format(
                    input_, datetime_format, tz=tz_dict
                )
                other_ambiguous_format_datetime = from_pendulum_format(
                    input_, other_datetime_format, tz=tz_dict
                )
                if input_ != other_ambiguous_format_datetime:
                    raise AmbiguousDatetimeFormatsError(
                        f"""
                        Ambiguity found between datetime formats [{datetime_format}] and
                        [{other_datetime_format}]. Formats parsed [{ambiguous_datetime}]
                        to [{ambiguous_format_datetime}] and
                        [{other_ambiguous_format_datetime}], respectively.
                        """
                    )
            except ValueError:
                # Ignoring ValueError because we're not concerned about validity of
                # parses in this function
                pass
            except AssertionError:
                # Ignoring AssertionErrors because we're not concerned about
                # validity of parses in this function
                pass
