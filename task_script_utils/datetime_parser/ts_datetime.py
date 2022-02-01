import copy
from datetime import datetime
from typing import Optional

import pendulum

from .parser_exceptions import AmbiguousFoldError


class TSDatetime:
    def __init__(self, datetime_: datetime, subseconds: Optional[str] = None):
        if not isinstance(datetime_, datetime):
            raise TypeError("datetime_ must be a datetime object")

        self._datetime = datetime_
        self._subseconds = subseconds

    @property
    def tzinfo(self):
        return self._datetime.tzinfo

    @property
    def datetime(self):
        """Return a new `datetime` object after replacing `microseconds`
        with `self._subseconds` in `self._datetime`.
        `subseconds` needs to be truncated to 6 digits
        """
        if self._subseconds is None:
            return self._datetime

        microseconds = self._subseconds[:6]
        microseconds = datetime.strptime(microseconds, "%f").microsecond
        new_datetime = self._datetime.replace(microsecond=microseconds)
        return new_datetime

    def tsformat(self):
        """Returns datetime string in Tetrascience's ISO8601 DateTime
        format"""
        minimal_format = "YYYY-MM-DDTHH:mm:ss"

        if self.tzinfo is not None:
            utc = pendulum.tz.UTC
            utc_date = utc.convert(self._datetime)
            iso_8601 = utc_date.format(minimal_format)
            if self._subseconds is not None:
                iso_8601 = f"{iso_8601}.{self._subseconds}"
            iso_8601 = f"{iso_8601}Z"
        else:
            iso_8601 = self._datetime.format(minimal_format)
            if self._subseconds is not None:
                iso_8601 = f"{iso_8601}.{self._subseconds}"

        return iso_8601

    def isoformat(self):
        """Returns datetime string in ISO format with offset values"""
        iso_str = self._datetime.format("YYYY-MM-DDTHH:mm:ss")
        if self._subseconds:
            iso_str += f".{str(self._subseconds)}"
        if self.tzinfo:
            offset = self._datetime.format("ZZ")
            if ":" not in offset:
                offset = f"{offset[:3]}:{offset[-2:]}"
            iso_str += offset
        return iso_str

    def change_fold(self, new_fold: int):
        if new_fold is None and self._is_fold_required:
            raise AmbiguousFoldError(
                "DatetimeConfig.fold must not be None to parse datetime without ambiguity."
            )

        if self._datetime.tzinfo is None or new_fold == self._datetime.fold:
            return

        self._datetime = self._datetime.replace(fold=new_fold)

    @property
    def _is_fold_required(self) -> bool:
        """Check whether an undefined `fold` would cause an ambiguous TSDatetime
        This function returns True if "fold" is required to disambiguate a
        datetime, False otherwise.
        """
        # Copy because TSDatetime is mutable
        dt = copy.deepcopy(self)
        dt.change_fold(0)
        dt_before_fold = dt.tsformat()
        dt.change_fold(1)
        dt_after_fold = dt.tsformat()
        return dt_before_fold != dt_after_fold
