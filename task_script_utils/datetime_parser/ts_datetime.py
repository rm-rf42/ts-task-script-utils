from datetime import datetime
from typing import Optional

import pendulum


class TSDatetime:
    def __init__(
        self,
        datetime_: datetime,
        subseconds: Optional[int] = None
    ):
        if not isinstance(datetime_, datetime):
            raise TypeError("datetime_ must be a datetime object")

        self._datetime = datetime_
        self._subseconds = subseconds

    @property
    def tzinfo(self):
        return self._datetime.tzinfo

    @property
    def datetime(self):
        if self._subseconds is None:
            return self._datetime

        microseconds = int(str(self._subseconds)[:6])
        new_datetime = self._datetime.replace(microsecond=microseconds)
        return new_datetime

    @property
    def ts_format(self):
        minimal_format = "YYYY-MM-DDTHH:mm:ss"

        if self.tzinfo is not None:
            utc = pendulum.tz.UTC
            utc_date = self._datetime
            utc_date = utc.convert(utc_date)
            iso_8601 = utc_date.format(minimal_format)
            if self._subseconds is not None:
                iso_8601 = f"{iso_8601}.{self._subseconds}"
            iso_8601 = f"{iso_8601}Z"
        else:
            iso_8601 = self._datetime.format(minimal_format)
            if self._subseconds is not None:
                iso_8601 = f"{iso_8601}.{self._subseconds}"

        return iso_8601

    @property
    def iso_format(self):
        iso_str = self._datetime.format("YYYY-MM-DDTHH:mm:ss")
        if self._subseconds:
            iso_str += f".{str(self._subseconds)[:6]}"
        if self.tzinfo:
            offset = self._datetime.format("ZZ")
            if ":" not in offset:
                offset = f"{offset[:3]}:{offset[-2:]}"
            iso_str += offset
        return iso_str

    def change_fold(self, new_fold: int):
        if (
            self._datetime.tzinfo is None
            or new_fold is None
            or new_fold == self._datetime.fold
        ):
            return

        self._datetime = self._datetime.replace(fold=new_fold)

