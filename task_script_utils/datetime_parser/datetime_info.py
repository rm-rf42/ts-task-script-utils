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
