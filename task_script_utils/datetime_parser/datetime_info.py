import re
import json
from datetime import datetime as dt
from itertools import product
from typing import List, Optional, Tuple, Union

import pendulum
from pendulum.locales.en import locale
from pydash.arrays import flatten

from .parser_exceptions import *
from .datetime_config import DatetimeConfig
from .tz_list import _all_abbreviated_tz_list
from .ts_datetime import TSDatetime
from .utils import parse_with_formats

class DateTimeInfo:
    """This class performs two functions:
    1. If the datetime string passed is short, it tries to parse
    it using regex and `DatetimeConfig`. If parsing failed or it can not detect date and
    time with confidence, an Exception will be raised. The parsed `datetime` object can be
    accessed via `DatetimeInfo.datetime

    2. If the datetime string passed is a long, It will detect the formatting
    tokens and their relative position in order to build a list datetime format that can be used
    to parse the datetime string. eg for "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata",
    `_parse_long_date_formats()` will detect token used are `DDDD`, `MMM` and `Do` and also that
    day of the week comes first or not.
    """

    def __init__(self, date_time_raw: str, config: DatetimeConfig):
        self.date_time_raw: str = date_time_raw
        self.config: DatetimeConfig = config

        self.am_or_pm: Optional[str] = None
        self.iana_tz: Optional[str] = None
        self.offset_: Optional[str] = None
        self.abbreviated_tz: Optional[str] = None
        self.day: Optional[str] = None
        self.month: Optional[str] = None
        self.year: Optional[str] = None
        self.hour: Optional[str] = None
        self.minutes: Optional[str] = None
        self.seconds: Optional[str] = None
        self.fractional_seconds: Optional[str] = None

        self.parsed_datetime: Optional[TSDatetime] = None
        self.parsed_datetime_format: Optional[str] = None
        self.date_time_processed: str = self._pre_process_datetime_string()


    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def _parse(self, matchers):
        _matchers = list(matchers)
        tokens = self.date_time_raw.split()
        for token in tokens:
            for func in _matchers:
                result = func(token)
                if result:
                    # It means result of func(token)
                    # has matched something and we don't
                    # need that matcher anymore. Hence
                    # remove it from the _matcher list
                    _matchers.remove(func)

    def _pre_process_datetime_string(self):
        """This method is used to pre-process the input string
        if required, before the parsing starts. It performs following
        pre-processing:
        1. Repace a character if it is sandwiched between two integer
        """
        raw_dt = self.date_time_raw
        raw_dt = self._replace_single_characters(raw_dt)
        self.date_time_processed = raw_dt

    def _replace_single_characters(self, string: str):
        # Input =  2018-13-09T11:12:23.000-05:30
        # output = 2018-13-09 11:12:23.000-05:30
        char_list = list(string)
        for i, current_char in enumerate(char_list[1:-1]):
            if (
                char_list[i - 1].isdigit()
                and char_list[i].isalpha()
                and char_list[i + 1].isdigit()
            ):
                char_list[i] = " "

        return "".join(char_list)

    @property
    def offset(self):
        """
        Return UTC offset that was found during parsing
        """
        if self.offset_:
            return self.offset_

        if self.abbreviated_tz:
            if self.abbreviated_tz not in self.config.tz_dict:
                raise OffsetNotKnownError(
                    f"Offset value not known for '{self.abbreviated_tz}'"
                )
            return self.config.tz_dict[self.abbreviated_tz]

        return None

    @property
    def dtstamp(self):
        """Created Datetime string from parsed raw input string.
        The format is DD-MM-YYYY hh:mm:ss and fractional seconds (upto 6 digit), AM/PM
        and utc offset are appended conditionally

        Returns:
            str/None: A datetime string
        """
        if self.parsed_datetime:
            return self.parsed_datetime.isoformat()

        if (
            self.day
            and self.month
            and self.year
            and self.hour
            and self.minutes
            and self.seconds
        ):
            dt_str = f"{self.year}-{self.month}-{self.day}"
            dt_str += f" {self.hour}:{self.minutes}:{self.seconds}"
            if self.fractional_seconds:
                # This property along with dt_format is used to create
                # a datetime object. Since python datetime support 6 digits for
                # microseconds, therefore truncating fraction seconds to 6 digits
                dt_str += f".{self.fractional_seconds[:6]}"

            if self.am_or_pm and int(self.hour) <= 12:
                dt_str += f" {self.am_or_pm.upper()}"

            if self.offset:
                dt_str += f" {self.offset}"
            if self.iana_tz:
                dt_str += f" {self.iana_tz}"

            return dt_str

        return None

    @property
    def datetime_format(self):
        """Build datetime format using pendulum tokens.
        This property along with `dtstamp` property can be used
        to parse date using `pendulum.from_format`.

        Returns:
            str: A datetime format build using pendulum formatting
            tokens. This string represent the datetime format for
            `dtstamp`
        """
        if self.parsed_datetime_format:
            return self.parsed_datetime_format

        if not self.dtstamp:
            return None

        day = "D" if len(self.day) == 1 else "DD"
        month = "M" if len(self.month) == 1 else "MM"
        year = "YYYY"

        if self.am_or_pm and int(self.hour) <= 12:
            hrs = "h" if len(self.hour) == 1 else "hh"
        else:
            hrs = "H" if len(self.hour) == 1 else "HH"
        mins = "m" if len(self.minutes) == 1 else "mm"
        seconds = "s" if len(self.seconds) == 1 else "ss"
        fmt = f"{year}-{month}-{day} {hrs}:{mins}:{seconds}"

        if self.fractional_seconds:
            # Pendulum support upto 6 fractional seconds
            fmt += "." + ("S" * len(self.fractional_seconds[:6]))
        if self.am_or_pm and int(self.hour) <= 12:
            fmt += " A"
        if self.offset:
            fmt += " Z"
        if self.iana_tz:
            fmt += " z"

        self.__parsed_datetime_format = fmt
        return fmt

    @property
    def datetime(self):
        if self.parsed_datetime:
            return self.parsed_datetime

        if not self.datetime_format or not self.dtstamp:
            return None

        datetime_ = pendulum.from_format(self.dtstamp, self.dt_format, tz=None)
        self.datetime = TSDatetime(datetime_=datetime_, subseconds=self.fractional_seconds)
        return self.datetime

    @datetime.setter
    def datetime(self, ts_datetime: TSDatetime):
        datetime_ = ts_datetime.datetime
        attrs = [
            "day", "month", "year", "hour", "minute", "second"
        ]
        for attr in attrs:
            val = getattr(datetime_, attr)
            setattr(self, attr, str(val))

        self.fractional_seconds = ts_datetime._subseconds
        self.parsed_datetime = ts_datetime

class LongDateTimeInfo(DateTimeInfo):
    def __init__(self, date_time_raw: str, config: DatetimeConfig):
        super().__init__(date_time_raw, config)

        self.token_day_of_week: Optional[str] = None
        self.token_day: Optional[str] = None
        self.token_month: Optional[str] = None
        self.has_fractional_seconds: Optional[str] = None

        self._parse_long_date_formats()

    def _parse_long_date_formats(self):
        matchers = [
            self._match_day_of_week_token,
            self._match_month_token,
            self._match_day_token,
            self._match_fractional_seconds,
        ]
        self._parse(matchers)
        if self.token_day is None:
            self.token_day = "DD"

        long_datetime_formats = self._build_long_datetime_formats_list()
        parsed_datetime, matched_format = parse_with_formats(
            datetime_str=self.date_time_raw,
            datetime_config=self.config,
            formats=long_datetime_formats,
        )
        if parsed_datetime:
            self.datetime = parsed_datetime
            self.parsed_datetime_format = matched_format

    def _match_day_of_week_token(self, token: str) -> bool:
        days = locale.locale["translations"]["days"]
        token_map = {
            "dddd": days["wide"].values(),
            "ddd": days["abbreviated"].values(),
            "dd": days["short"].values(),
        }
        token = self._get_token(token, token_map)
        if token is not None:
            self.token_day_of_week = token
            return True
        return False

    def _match_month_token(self, date_time_token: str) -> bool:
        months = locale.locale["translations"]["months"]
        token_map = {
            "MMMM": months["wide"].values(),
            "MMM": months["abbreviated"].values(),
        }
        token = self._get_token(date_time_token, token_map)
        if token is not None:
            self.token_month = token
            return True
        return False

    def _match_day_token(self, date_time_token: str) -> bool:
        ordinals = ["st", "nd", "rd", "th"]
        token = None
        for val in ordinals:
            if date_time_token.endswith(val):
                token = "Do"
            elif date_time_token.endswith(f"{val},"):
                token = "Do,"
        if token is not None:
            self.token_day = token
            return True
        return False

    def _match_fractional_seconds(self, token):
        fraction_pattern = r"\d+\.\d+"
        matches = re.findall(fraction_pattern, token)
        if len(matches) == 1:
            match = matches[0]
            self.fractional_seconds = match.split(".")[1]
            return True
        return False

    def _get_token(self, token, token_map: dict):
        for key_, values in token_map.items():
            if token in values:
                return key_
            elif token.replace(",", "") in values:
                return f"{key_},"
        return None

    def _build_long_date_format(self):
        """Use DatetimeInfo to build and return date format for
        log datetime string.

        Raises:
            InvalidDateError: Raised if parsing fails to
            detect tokens for month or day

        Returns:
            str: Return Date format built using pendulum
            formatting tokens
        """
        if not (self.token_month and self.token_day):
            raise InvalidDateError(f"{self.date_time_raw}")

        if self.token_day_of_week:
            date_fmt = (
                f"{self.token_day_of_week} "
                f"{self.token_month} "
                f"{self.token_day} "
                f"YYYY"
            )
        else:
            date_fmt = f"{self.token_month} {self.token_day} YYYY"
        return date_fmt

    def _build_time_formats(self, fractional_seconds):
        TIME_PARTS = [
            ["h", "hh", "H", "HH"],
            ["m", "mm"],
            ["s", "ss"],
        ]

        def map_am_pm(time_format):
            return time_format if time_format.startswith("H") else time_format + " A"

        time_formats = [":".join(tokens) for tokens in product(*TIME_PARTS)]
        if self.fractional_seconds:
            token = "SSSSSS"
            time_formats = map(lambda x: [x, f"{x}.{token}"], time_formats)

        time_formats = flatten(time_formats)
        time_formats = map(lambda x: map_am_pm(x), time_formats)
        time_formats = map(
            lambda x: [x, x + " Z", x + " z", x + " ZZ", x + " Z z", x + " ZZ z"],
            time_formats,
        )
        time_formats = flatten(time_formats)
        return tuple(time_formats)

    def _build_long_datetime_formats_list(self) -> Tuple[str]:
        """Returns a list of long datetime formats built
        using pendulum formatting tokens.
        """
        parts = [
            [self._build_long_date_format()],
            self._build_time_formats(self.fractional_seconds),
        ]
        formats = tuple(" ".join(values) for values in product(*parts))
        return formats
