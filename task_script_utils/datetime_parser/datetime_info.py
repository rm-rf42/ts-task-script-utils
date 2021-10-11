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
        }
        return methods_dict

    def match_iana_tz(self, token: str):
        if token in pendulum.timezones:
            return token

