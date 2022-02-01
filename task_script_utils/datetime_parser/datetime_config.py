from typing import Optional
from .utils import map_offset_to_seconds


class DatetimeConfig:
    def __init__(
        self,
        day_first: Optional[bool] = None,
        year_first: Optional[bool] = None,
        tz_dict: dict = {},
        fold: Optional[int] = None,
    ):
        """DatetimeConfig provides complementary information on how to mark
        parsed digits as day, month or year.
        It also provides an option to handle abbreviated time zones and
        fold for parsing ambiguous timestamps during daylight saving transitions.
        Ideally, DatetimeConfig should be constructed from pipeline configuration
        passed to task scripts.

        Args:
            day_first (Optional[bool], optional): Whether to interpret the first
            value in an ambiguous 3-integer date (e.g. 01/05/09) as the
            day (True) or month (False). Defaults to None.

            year_first (Optional[bool], optional): Whether to interpret the first
            value in an ambiguous 3-integer date (e.g. 01/05/09) as the year.
            Defaults to None. When the year has four digits, then whether
            `year_first` is `true` or `false`,is decided by regex parsing done
            by `DatetimeInfo` class. If both `year_first` and `day_first` are true,
            then `year_first` will take priority and resulting date format will be as YDM.

            tz_dict (dict, optional): A python dict that maps abbreviated timezone
            names to their corresponding offset. Defaults to {}.

            fold (Optional[int], optional): 0 or 1. It is required during the
            2 hour window when clocks are set back in a timezone which keeps
            track of daylight savings (such as IANA timezones like `Europe/London`).
            Defaults to None.
        """
        self.day_first = day_first
        self.year_first = year_first
        self.tz_dict = tz_dict
        self.tz_dict_seconds = map_offset_to_seconds(tz_dict)
        self.fold = fold

    def __str__(self):
        return (
            f"day_first={self.day_first}, "
            f"year_first={self.year_first}, "
            f"fold={self.fold}, "
            f"tz_dict={self.tz_dict}"
        )


DEFAULT_DATETIME_CONFIG = DatetimeConfig()
