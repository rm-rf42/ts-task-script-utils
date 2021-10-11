import re
import json
from typing import Union

import pendulum

from .parser_exceptions import *
from .pipeline_config import PipelineConfig


class DateTimeInfo:
    def __init__(self, date_time_raw: str, config: PipelineConfig):
        self.date_time_raw = date_time_raw
        self.am_or_pm = None
        self.short_date = None
        self.time = None
        self.iana_tz = None
        self.day_first = None
        self.year_first = None
        self.month_first = None
        self.offset = None
        self.military_format = None
        self.config = config
        self.parse()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def parse(self):
        checks = self.get_checks()
        tokens = self.date_time_raw.split(" ")
        for token in tokens:
            t = token
            for var_name, func in checks.items():
                if getattr(self, var_name) is None:
                    result = func(token)
                    if result:
                        setattr(self, var_name, result)

    def get_checks(self):
        methods_dict = {
            "iana_tz": self.match_iana_tz,
            "time": self.match_time,
            "short_date": self.match_short_date,
        }
        return methods_dict

    def match_iana_tz(self, token: str):
        if token in pendulum.timezones:
            return token

    def match_time(self, token: str):
        pattern = r"\d+:\d+:\d+.\d+|\d+:\d+:\d+"
        matches = re.findall(pattern, token)
        if not matches:
            return None

        if len(matches) > 1:
            raise MultipleTimesFoundError(
                f"Multiple Time values found: {matches}")
        time_ = matches[0].split(":")
        hour, minutes, seconds = time_
        if "." in seconds:
            seconds, milliseconds = seconds.split(".")
        else:
            milliseconds = None

        assert (0 <= int(hour) <= 24), InvalidTimeError(
            f"Invalid time : {time_}. Hours value is incorrect")
        assert (0 <= int(minutes) <= 60), InvalidTimeError(
            f"Invalid time : {time_}. Minutes value is incorrect")
        assert (0 <= int(seconds) <= 60), InvalidTimeError(
            f"Invalid time : {time_}. Seconds value is incorrect")

        self.hour = int(hour)
        self.minutes = int(minutes)
        self.seconds = int(seconds)
        self.milliseconds = int(milliseconds)
        return ':'.join(time_)

    def match_short_date(self, token: str) -> Union[tuple, None]:
        year_first_pattern = r"\d{4,4}[-~!@#$%^&*.,;/\\]\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}"
        year_last_pattern = r"\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}[-!~@#$%^&*.,;/\\]\d{4,4}"
        two_digit_date_pattern = r"\d{1,2}[-~!@#$%^&*.,;/\\]\d{1,2}[-!~@#$%^&*.,;/\\]\d{1,2}"
        no_sep_date_pattern = r"\d{6,6}"

        # YYYY-XX-XX
        year_first_matches = re.findall(year_first_pattern, token)
        if year_first_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_first_matches, True)
            self.day, self.month, self.year = day, month, year
            return f"{year}-{month}-{day}"

        # XX-XX-YYYY
        year_last_matches = re.findall(year_last_pattern, token)
        if year_last_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_last_matches, False)
            self.day, self.month, self.year = day, month, year
            return f"{year}-{month}-{day}"

        # Cases = [XX-XX-XX, XX-X-X, X-X-XX, X-X-X]
        two_digit_date_pattern_matches = re.findall(
            two_digit_date_pattern, token)
        if two_digit_date_pattern_matches:
            day, month, year = self._process_two_digit_date_pattern(
                two_digit_date_pattern_matches)
            self.day, self.month, self.year = day, month, year
            return f"{year}-{month}-{day}"

        return None

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

        day, month = self._process_day_and_month(others)
        year = int(year)
        return day, month, year

    def _process_two_digit_date_pattern(self, matches):
        if len(matches) > 1:
            raise MultipleDatesError(f"Multiple Dates Detected: {matches}")

        date = re.sub(r"[-~!@#$%^&*.,;/\\]", "-", matches[0])
        date_tokens = [i for i in date.split("-")]

        if self.config.year_first is True:
            if self.config.day_first is True:
                # Input = YY-DD-MM
                year, day, month = date_tokens
            elif self.config.day_first is False:
                # Input = YY-MM-DD
                # TODO: How to handle 01-15-11
                year, month, day = date_tokens
            else:
                year, other_tokens = date_tokens[0], date_tokens[1:]
                day, month = self._process_day_and_month(other_tokens)
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
                day, others = date_tokens[0], date_tokens[1:]
                month, year = self._decide_month_and_year(others)
            elif self.config.day_first is False:
                # This could be MM-DD-YY, YY-MM-DD
                # Ambiguous
                raise AmbiguousDateError(
                    f"AmbiguousDateError: Date={matches[0]}; year_first=None; day_first=False")
            else:
                # Could Be MM-DD-YY, DD-MM-YY
                # Could Be YY-DD-MM, YY-MM-DD
                # Could Be DD-YY-MM, MM-YY-DD
                raise AmbiguousDateError(
                    f"AmbiguousDateError: Date={matches[0]}; year_first=None; day_first=None")

        assert 0 < int(month) <= 12, InvalidDateError(
            f"Invalid month: {month}, Date={matches[0]}, year_first={self.config.year_first}, day_first={self.config.day_first}"
        )
        assert 0 < int(day) <= 31, InvalidDateError(
            f"Invalid day: {day}, Date={matches[0]}, year_first={self.config.year_first}, day_first={self.config.day_first}"
        )

        if len(year) == 1:
            year = f"200{year}"
        else:
            year = f"20{year}"

        return day, month, year

    def _process_day_and_month(self, tokens):
        tokens = [int(token) for token in tokens]

        first_token_is_month = tokens[0] <= 12
        second_token_is_month = tokens[1] <= 12

        if first_token_is_month and second_token_is_month:
            raise AmbiguousDateError(
                f"Can't decide day and month between: {tokens}")

        if not first_token_is_month and not second_token_is_month:
            # Both tokens could be month
            raise AmbiguousDateError(
                f"Can't decide day and month between: {tokens}")

        day, month = (
            (tokens[0], tokens[1])
            if second_token_is_month
            else (tokens[1], tokens[0])
        )
        day = f"0{day}" if day < 10 else str(day)
        month = f"0{month}" if month < 10 else str(month)
        return day, month

    def _decide_month_and_year(self, tokens):
        first_token_is_month = int(tokens[0]) <= 12
        second_token_is_month = int(tokens[1]) <= 12

        if first_token_is_month and second_token_is_month:
            raise AmbiguousDateError(
                f"Can't decide month and year between: {tokens}")

        if not first_token_is_month and not second_token_is_month:
            # Both tokens could be month
            raise AmbiguousDateError(
                f"Can't decide month and year between: {tokens}")

        day, month = (
            (tokens[0], tokens[1])
            if first_token_is_month
            else (tokens[1], tokens[0])
        )
        day = f"0{day}" if day < 10 else str(day)
        month = f"0{month}" if month < 10 else str(month)
        return day, month
