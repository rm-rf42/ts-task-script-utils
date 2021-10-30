from datetime import datetime as dt
import re
import json
from typing import List, Union

import pendulum

from .parser_exceptions import *
from .pipeline_config import PipelineConfig


class DateTimeInfo:
    def __init__(self, date_time_raw: str, config: PipelineConfig):
        self.date_time_raw = date_time_raw
        self._pre_process_datetime_string()
        self.am_or_pm = None
        self.iana_tz = None
        self.offset_ = None
        self.abbreviated_tz = None
        self.day = None
        self.month = None
        self.year = None
        self.hour = None
        self.minutes = None
        self.seconds = None
        self.milliseconds = None
        self.config = config

        self.parse()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def parse(self):
        checks = self._get_checks()
        tokens = self.date_time_raw.split()
        for token in tokens:
            for var_name, func in checks.items():
                if getattr(self, var_name) is None:
                    result = func(token)
                    if result and isinstance(result, dict):
                        for key, value in result.items():
                            setattr(self, key, value)
                    elif result is not None:
                        setattr(self, var_name, result)

        # if self.iana_tz:
        #    self.offset_ = pendulum.now(tz=self.iana_tz).format("Z")

    def _get_checks(self):
        """It creates a `dict` that maps parsing functions to instance
        variable that should store the result.

        eg. if `self.match_short_date` is able to parse short
        date successfully, it will be stored in `self.short_date`
        """
        methods_dict = {
            "iana_tz": self._match_iana_tz,
            "time_str": self._match_time,
            "date_str": self._match_short_date,
            "am_or_pm": self._match_am_or_pm,
            "offset_": self._match_offset,
            "abbreviated_tz": self._match_tz_abbreviation
        }
        return methods_dict

    def _match_iana_tz(self, token: str) -> str:
        """Match and store IANA timezone

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            str : An IANA timezone string
        """
        if token in pendulum.timezones:
            return token

    def _match_time(self, token: str) -> Union[str, None]:
        """Use Regex to find any time string present in
        input token

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Raises:
            - MultipleTimesFoundError: When more than one time-string
            are matched
            - InvalidTimeError: When time like string is parsed, but the
            numeric value of hrs, minutes and seconds are out of bound.

        Returns:
            Union[str, None]: return if any time string is found
            else return None
        """
        hh_mm_ss_pattern = r"\d+:\d+:\d+.\d+|\d+:\d+:\d+"
        hh_mm_pattern = r"^(?![+-])\d{1,2}:\d{1,2}"

        matches = re.findall(hh_mm_ss_pattern, token)
        if not matches:
            matches = re.findall(hh_mm_pattern, token)
            if not matches:
                return None

        if len(matches) > 1:
            raise MultipleTimesFoundError(
                f"Multiple Time values found: {matches}")

        time_ = matches[0].strip()
        time_ = time_.replace("+", "")
        time_ = time_.replace("-", "")
        time_ = time_.split(":")

        if len(time_) == 2:
            hour, minutes = time_
            seconds = "00"
        else:
            hour, minutes, seconds = time_
        if "." in seconds:
            seconds, milliseconds = seconds.split(".")
            # TODO: differentiate between milliseconds and microseconds
            # see if `pendulum` has a generic way of handling fractional
            # seconds
        else:
            milliseconds = None

        if not (0 <= int(hour) <= 24):
            raise InvalidTimeError(
                f"Invalid time : {time_}. Hours value is incorrect")
        if not (0 <= int(minutes) <= 60):
            raise InvalidTimeError(
                f"Invalid time : {time_}. Minutes value is incorrect")
        if not (0 <= int(seconds) <= 60):
            raise InvalidTimeError(
                f"Invalid time : {time_}. Seconds value is incorrect")

        return {
            "hour": hour,
            "minutes": minutes,
            "seconds": seconds,
            "milliseconds": milliseconds
        }

    def _match_short_date(self, token: str) -> Union[str, None]:
        """Use Regex to find any short date string present in
        input token

        If a valid, non-ambiguous match is found, then it also sets
        `self.day`, `self.month` and `self.year`

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Union[str, None]: if a match occurs return DD-MM-YYYY formated
            date string else return None
        """
        year_first_pattern = r"\d{4,4}[-~!@#$%^&*.,;/\\]\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}"
        year_last_pattern = r"\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}[-!~@#$%^&*.,;/\\]\d{4,4}"
        two_digit_date_pattern = r"\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}[-!~@#$%^&*.,;/\\]\d{1,2}"
        # no_sep_date_pattern = r"\d{6,6}"

        # YYYY-XX-XX
        year_first_matches = re.findall(year_first_pattern, token)
        if year_first_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_first_matches, True)
            self.day, self.month, self.year = day, month, year
            return {
                "year": year,
                "month": month,
                "day": day
            }

        # XX-XX-YYYY
        year_last_matches = re.findall(year_last_pattern, token)
        if year_last_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_last_matches, False)
            self.day, self.month, self.year = day, month, year
            return {
                "year": year,
                "month": month,
                "day": day
            }

        # Cases = [XX-XX-XX, XX-X-X, X-X-XX, X-X-X]
        two_digit_date_pattern_matches = re.findall(
            two_digit_date_pattern, token)
        if two_digit_date_pattern_matches:
            day, month, year = self._process_two_digit_date_pattern(
                two_digit_date_pattern_matches)

            return {
                "year": year,
                "month": month,
                "day": day
            }

        return None

    def _match_offset(self, token: str) -> Union[str, None]:
        """Use Regex to find if any utc offset value
        is present in input token

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Union[str, None]: +hh:mm or -hh:mm if a match is found
            else None
        """
        # Can't parse 12-23-1223T11:12:23.000-05:30
        # offset with - sign, confuses with date separator
        # that why we need space 12-23-1223T11:12:23.000 -05:30
        patterns = [
            r"[Uu][Tt][Cc][+-]\d+",
            r"[+-]\d{1,2}:\d{1,2}",
            r"[+-]\d{1,2}",
        ]

        # if the token matched short date
        # then it is a date don't match for offset
        try:
            short_date = self._match_short_date(token)
        except Exception as e:
            short_date = None

        if short_date:
            return None

        for pattern in patterns:
            matches = re.findall(pattern, token)
            if matches:
                if len(matches) != 1:
                    return MultipleOffsetsError(f"Multiple offsets found: {matches}")
                match = matches[0].strip()
                if match.lower().startswith("utc"):
                    match = match[3:]
                sign, offset = match[0], match[1:]
                offset = self._pad_and_validate_offset_value(offset)
                if offset:
                    return f"{sign}{offset}"
        return None

    def _match_am_or_pm(self, token: str):
        """
        Use regex to check if input string contains
        AM or PM. Return the matched value
        """
        pattern = r"[ap][m]$"
        matches = re.findall(pattern, token, flags=re.IGNORECASE)
        if not matches or len(matches) != 1:
            return None
        return matches[0].upper()

    def _match_tz_abbreviation(self, token: str) -> Union[str, None]:
        """ Check if the input token is an abbreviated timezone
        present in Pipeline Config's tz_dict

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Union[str, None]: string like CST/EST etc if a
            match is found else None
        """
        if not self.config.tz_dict_seconds:
            return None
        for tz in self.config.tz_dict_seconds.keys():
            if tz == token.upper():
                return tz
        return None

    @property
    def date_str(self):
        """Returns YYYY-MM-DD"""
        if (
            self.day
            and self.month
            and self.year
        ):
            return f"{self.year}-{self.month}-{self.day}"

    @property
    def time_str(self):
        """Returns:
            - Hours:Minutes:seconds
            - Hours:Minutes:seconds.Fraction
        """
        if not (
            self.hour
            and self.minutes
            and self.seconds
        ):
            return None

        result = f"{self.year}-{self.month}-{self.day}"
        if self.milliseconds:
            result = f"{result}.{self.milliseconds}"

        return result

    @property
    def offset(self):
        """
        Return UTC offset that was found during parsing
        """
        if self.offset_:
            return self.offset_

        if self.abbreviated_tz:
            return self.config.tz_dict[self.abbreviated_tz]

        if self.iana_tz:
            return pendulum.now(tz=self.iana_tz).format("Z")

        return None

    @property
    def dtstamp(self):
        """Created Datetime string from parsed raw input string.
        The format is DD-MM-YYYY hh:mm:ss and milliseconds, AM/PM
        and utc offset are appended conditionally

        Returns:
            str/None: A datetime string
        """
        if (
            self.day
            and self.month
            and self.year
            and self.hour
            and self.minutes
            and self.seconds
        ):
            dt_str = f"{self.day}-{self.month}-{self.year}"
            dt_str += f" {self.hour}:{self.minutes}:{self.seconds}"
            if self.milliseconds:
                dt_str += f".{self.milliseconds}"

            if self.am_or_pm and int(self.hour) <= 12:
                dt_str += f" {self.am_or_pm.upper()}"

            if self.offset:
                dt_str += f" {self.offset}"
            return dt_str

        return None

    @property
    def dt_format(self):
        """Build datetime format using pendulum tokens.
        This property along with `dtstamp` property can be used
        to parse date using `pendulum.from_format`

        Returns:
            str: A datetime format build using pendulum formatting
            tokens. This string represent the datetime format for
            `dtstamp`
        """
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
        fmt = f"{day}-{month}-{year} {hrs}:{mins}:{seconds}"

        if self.milliseconds:
            fmt += ".SSS"
        if self.am_or_pm and int(self.hour) <= 12:
            fmt += " A"
        if self.offset:
            fmt += " Z"
        return fmt

    @property
    def datetime(self):
        if not self.dt_format or not self.dtstamp:
            return None
        return pendulum.from_format(
            self.dtstamp,
            self.dt_format,
            tz=None
        )

    def _pre_process_datetime_string(self):
        """This method is used to pre-process the input string
        if required, before the parsing starts. It performs following
        pre-processing:
        1. Repace a character if it is sandwiched between two integer
        """
        raw_dt = self.date_time_raw
        raw_dt = self._replace_single_characters(raw_dt)
        self.date_time_raw = raw_dt

    def _process_year_first_or_last_matches(self, matches, year_first):
        if len(matches) > 1:
            raise MultipleDatesError(f"Multiple Dates Detected: {matches}")

        date = re.sub(r"[-~!@#$%^&*.,;/\\]", "-", matches[0]).split("-")
        if year_first:
            year, others = date[0], date[1:]
        else:
            others, year = date[: -1], date[-1]

        if len(year) == 3:
            raise InvalidYearError(f"{date} has invalid year.")

        if self.config.day_first is True:
            day, month = others
        elif self.config.day_first is False:
            month, day = others
        else:
            day, month = self._process_day_and_month(others)

        # Validate day, year, month
        try:
            dt_date = dt(
                day=int(day),
                month=int(month),
                year=int(year)
            )
        except Exception as e:
            msg = f"{str(e)}, date={date}, config={self.config}"
            raise InvalidDateError(msg)

        return day, month, year

    def _process_two_digit_date_pattern(self, matches):
        if len(matches) > 1:
            raise MultipleDatesError(f"Multiple Dates Detected: {matches}")

        date = re.sub(r"[-~!@#$%^&*.,;/\\]", "-", matches[0])
        date_tokens = date.split("-")

        if self.config.year_first is True:
            if self.config.day_first is True:
                # Input = YY-DD-MM
                year, day, month = date_tokens
            else:
                # Input = YY-MM-DD
                year, month, day = date_tokens
        elif self.config.year_first is False:
            if self.config.day_first is True:
                # Input = DD-MM-YY
                day, month, year = date_tokens
            elif self.config.day_first is False:
                # Input = MM-DD-YY
                month, day, year = date_tokens
            else:
                # Input = XX-XX-YY
                year, other_tokens = date_tokens[-1], date_tokens[:-1]
                day, month = self._process_day_and_month(other_tokens)
        else:
            if self.config.day_first is True:
                # Input = DD-MM-YY
                day, month, year = date_tokens
            elif self.config.day_first is False:
                # Could Be MM-DD-YY or YY-MM-DD
                date_str = '-'.join([
                    f"{int(token):02d}"
                    for token in date_tokens
                ])
                day, month, year = self._try_formats(
                    date_str,
                    ["MM-DD-YY", "YY-MM-DD"]
                )
            else:
                # Could Be MM-DD-YY or YY-MM-DD or DD-MM-YY
                date_str = '-'.join([
                    f"{int(token):02d}"
                    for token in date_tokens
                ])
                day, month, year = self._try_formats(
                    date_str,
                    ["MM-DD-YY", "YY-MM-DD", "DD-MM-YY"]
                )

        if len(year) == 1:
            year = f"200{year}"
        elif len(year) == 2:
            year = f"20{year}"

        day = f"{int(day):02d}"
        month = f"{int(month):02d}"

        # Validate day, year, month
        try:
            dt_date = dt(
                day=int(day),
                month=int(month),
                year=int(year)
            )
        except Exception as e:
            msg = f"{str(e)}, date={date}, config={self.config}"
            raise InvalidDateError(msg)

        return day, month, year

    def _process_day_and_month(self, tokens: List[str]) -> tuple:
        """Given a list of two numeric tokens,
        try to decide which token is day and which
        is month.

        Args:
            tokens (List): a list containing two
            numeric tokens

        Raises:
            AmbiguousDateError: When we fail to decide between day and month


        Returns:
            tuple: (day, month)
        """

        first_token_is_month = int(tokens[0]) <= 12
        second_token_is_month = int(tokens[1]) <= 12

        if first_token_is_month and second_token_is_month:
            raise AmbiguousDateError(
                f"Can't decide day and month between: {tokens}"
            )

        if not first_token_is_month and not second_token_is_month:
            # Both tokens could be month
            raise AmbiguousDateError(
                f"Can't decide day and month between: {tokens}"
            )

        day, month = (
            (tokens[0], tokens[1])
            if second_token_is_month
            else (tokens[1], tokens[0])
        )
        return day, month

    def _pad_and_validate_offset_value(self, offset):
        if ":" in offset:
            # 5:30 --> 05:30
            # 05:30 --> 05:30
            if len(offset) == 4:
                return f"0{offset}"
            elif len(offset) == 5:
                return offset
            else:
                return None
        else:
            # 2 --> 02:00 | 09 --> 09:00 | 12 --> 12:00
            # 530 --> 05:30
            # 0930 --> 09:30 | 1200 --> 12:00
            if len(offset) == 1:
                return f"0{offset}:00"
            elif len(offset) == 2:
                return f"{offset}:00"
            elif len(offset) == 3:
                return f"0{offset[0]}:{offset[1:]}"
            elif len(offset) == 4:
                return f"{offset[:2]}:{offset[2:]}"
            else:
                return None

    def _replace_single_characters(self, string: str):
        # Input =  2018-13-09T11:12:23.000-05:30
        # output = 2018-13-09 11:12:23.000-05:30
        prev_char: str = ""
        indexes = []
        for i, current_char in enumerate(string[:-1]):
            next_char = string[i+1]
            if (
                prev_char.isdigit()
                and current_char.isalpha()
                and next_char.isdigit()
            ):
                indexes.append(i)
            prev_char = current_char

        new_string = ""
        for i in range(len(string)):
            if i in indexes:
                new_string += " "
            else:
                new_string += string[i]

        return new_string

    def _is_format(self, date_str: str, format: str):
        """Given a date string and a format,
        try to parse the date.

        Args:
            date_str (str): date string
            format (str): date format built using
            tokens used in `pendulum` library

        Returns:
            tuple: If date is parsed successfully return
            (True, datetime object) else return (False, None)
        """
        try:
            parsed = pendulum.from_format(date_str, format)
            return parsed
        except Exception as e:
            return None

    def _try_formats(self, date_str: str, formats: List[str]):
        """Given a date string and a list for formats, make sure
        sure only one of the format successfully parses the date.
        If multiple or no format parses the date, raise AmbiguousDateError
        Args:
            date_str (str): date string
            formats (List[str]): list of date format built using
            tokens used in `pendulum` library

        Raises:
            AmbiguousDateError: If multiple or no format parses the date,
            raise `AmbiguousDateError`


        Returns:
            tuple[str]: (day, month, year)
        """
        parsed_results = [
            self._is_format(date_str, format_)
            for format_ in formats
        ]

        parsed_results = list(filter(lambda x: x is not None, parsed_results))
        if len(parsed_results) != 1:
            raise AmbiguousDateError(
                f"Ambiguous date:{date_str}, possible formats: {formats}"
            )
        result = parsed_results[0]
        return (
            str(result.day),
            str(result.month),
            str(result.year)
        )
