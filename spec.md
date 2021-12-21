## Datetime Parser

`taskscript_utils.datetime_parser` exposes `parse()` and `convert_to_ts_iso8601()` methods for parsing string datetimes.

The `parse()` returns a `TSDatetime` object and accepts following arguements:

- `datetime_raw_str: str`: raw datetime string to be parsed.
- `formats_list (Sequence[str], optional)`: You can optionally pass a list of formats to try to parse datetime string. If `datetime_raw_str` doesn't matches with any format, the datetime parser will still try to parse `datetime_raw_str` with other methods such as using regex and trying long datetime format
- `config (DatetimeConfig, optional)`: You also have an options to pass `DatetimeConfig`. It provides complementary information on how to mark parsed digits as day, month or year and also provide an options to handle abbreviated time zones and fold for parsing ambiguous timestamps during daylight saving transitions. Ideally, DatetimeConfig should be constructed from pipeline configuration passed to task scripts

The `convert_to_ts_iso8601()` uses `parse()` internally to return parsed datetime in Tetrascience's ISO8601 format. It also accepts same arguments as that of `parse()`

## Limitations

1. It is not possible to parse just dates or just times alone.
   eg.`parse('2021-12-08')` or `parse('2021-12-08')` will raise `InvalidDateError`

## Parsing With Formats

```Python
from task_script_utils.datetime_parser import parse
datetime_formats_list = [
    "DD-MM-YY HH:mm:ss z",
]

# Case 1: when raw datetime string matches with one of the format in datetime_formats_list
>>> result = parse("21-12-20 12:30:20 Asia/Kolkata", formats_list=datetime_formats_list)
>>> result.tsformat()
'2020-12-21T07:00:20Z'
>>> result.isoformat()
'2020-12-21T12:30:20+05:30'

# Case 2: when raw datetime string doesn't match with one of the format in datetime_formats_list but can be parsed without any ambiguity
# In this case, it can be inferred that year is 2020, day is 21 and hence month is 12
# This is just an example and there could be multiple cases that may lead to ambiguity or invalid datetime.
# These are discussed in later sections of this documents
>>> result = parse("21-12-2020 12:30:20 PM America/Chicago", formats_list=datetime_formats_list)
>>> result.isoformat()
'2020-12-21T12:30:20-06:00'
>>> result.tsformat()
'2020-12-21T18:30:20Z'

# Case 3: when raw datetime string doesn't match with one of the format in datetime_formats_list and is ambiguous
# This is just an example and there could be multiple cases that may lead to ambiguity or invalid datetime.
# These are discussed in later sections of this documents
>>> result = parse("21-12-20 12:30:20 PM America/Chicago", formats_list=datetime_formats_list)
'''
Traceback (most recent call last):
 ...
task_script_utils.datetime_parser.parser_exceptions.AmbiguousDateError: Ambiguous date:21-12-20, possible formats: ('MM-DD-YY', 'YY-MM-DD', 'DD-MM-YY')
'''
```

## Parsing Fractional Seconds

You can use `SSSSSS` as token to parse any number on digits as fractional seconds.
`TSDatetime` object returned by `parse()` helps maintaining the precision of fractional seconds.

For example, in the examples below `result.isoformat()` and `result.tsformat()` maintains the number of digits in fractional seconds.
This is different from python's `datetime` object, which only allows 6 digits for microseconds.
This is visible as the result of `result.datetime.isoformat()`, where `result.datetime` property return pythonic `datetime` object

```python
>>> from task_script_utils.datetime_parser import parse
>>> datetime_formats_list = [
    "DD-MM-YY HH:mm:ss.SSSSSS z",
]

# Example 1
>>> result = parse("2021-12-13T13:00:12.19368293274 Asia/Kolkata")
>>> result.tsformat()
'2021-12-13T07:30:12.19368293274Z'
>>> result.isoformat()
'2021-12-13T13:00:12.19368293274+05:30'
>>> result.datetime.isoformat()
'2021-12-13T13:00:12.193682+05:30'

# Example 2
>>> result = parse("2021-12-13T13:00:12.1 Asia/Kolkata")
>>> result.isoformat()
'2021-12-13T13:00:12.1+05:30'
>>> result.tsformat()
'2021-12-13T07:30:12.1Z'
>>> result.datetime.isoformat()
'2021-12-13T13:00:12.100000+05:30'
```

## Parsing Abbreviated Timezones

The only way to parse timestamps(if parse-able) is by passing `DatetimeConfig` object with `tz_dict`.
`DatetimeConfig.tz_dict` is a `dict` mapping abbreviated_tz to offset value. Defaults to `empty dict`.

```python
>>> from task_script_utils.datetime_parser import (
  parse,
  DatetimeConfig
)
>>> sample_tz_dict = {
...     "IST": "+05:30",
...     "EST": "-05:00",
...     "CST": "-06:00",
... }
>>> dt_config = DatetimeConfig(
...     tz_dict=sample_tz_dict
... )
>>> result = parse("2021-12-25T00:00:00 IST", config=dt_config)
>>> result.isoformat()
'2021-12-25T00:00:00+05:30'
>>> result.tsformat()
'2021-12-24T18:30:00Z'

# An exception will be raised if DatetimeConfig.tz_dict doesn't contain the abbreviated tz
result = parse("2021-12-12 14:15:16 BRST", config=dt_config)
'''
Traceback (most recent call last):
...
task_script_utils.datetime_parser.parser_exceptions.OffsetNotKnownError: Offset value not known for 'BRST'
'''
```

`"Z"` can be used as token for capturing abbreviated timezones when using datetime_formats to prase the raw datetime string. Even in this case, for successful parsing, `DatetimeConfig.tz_dict` is required

```python
>>> dt_formats_list = [
...     "YYYY-MM-DD HH:mm:ss Z"
... ]
>>> result = parse("2021-12-12 14:15:16 CST", formats_list=dt_formats_list, config=dt_config)
>>> result.isoformat()
'2021-12-12T14:15:16-06:00'
# Similar to example above, an exception will be raised if DatetimeConfig.tz_dict doesn't contain the abbreviated tz.

```
## Ambiguous Dates

If `formats_list` doesn't contain a match or is not passed, `parse` will use regex to parse the raw datetime string.
The regex parsing allows to capture digits of short formatted dates. The captured digits can all be two digits or one of them could be 4 digits long representing year.
Sometimes, it is hard to infer day, month and year from the parsed digits and this leads to ambiguity during parsing.

Following are some examples of ambiguous cases

| Cases      | Date Parts     | Reason for ambiguity                                              |
| ---------- | -------------- | ----------------------------------------------------------------- |
| 21-12-2    | [21, 12, 2]    | possible formats: ('MM-DD-YY', 'YY-MM-DD', 'DD-MM-YY')            |
| 21-23-2020 | [21, 21, 2020] | Year = 2020, but Can't decide day and month between: ('21', '23') |
| 2021-23-13 | [2021, 23, 13] | Year = 2021, but Can't decide day and month between: ('23', '13') |

## Resolving Ambiguous Dates with `DatetimeConfig`

After parser has extracted date parts using regex, `DatetimeConfig` can be used to handle ambiguous cases by specifying flags like `year_first: Optional[bool]` and `day_first: Optional[bool]`.

- `day_first: Optional[bool]`: `True/False`. Defaults to `None`
  - Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the day (True) or month (False).
- `year_first: Optional[bool]`: `True/False`. Defaults to `None`
  - Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the year.

Following resolution matrix specifies the possible datetime formats depending on the values of `day_first` and `year_first`.
| day_first(down)/ year_first | True | False | None |
| --------------------------- | ---------------------- | ---------------------- | ------------------------------------ |
| **True** | year-day-month | day-month-year | day-month-year |
| **False** | year-month-day | month-day-year | year-month-day <br> month-day-year |
| **None** | year-month-day <br> year-day-month | month-day-year <br> day-month-year | month-day-year <br> day-month-year <br> year-month-day |

- When `year_first` is `true` and day_first is `None` , `year-month-day` takes precedence over `year-day-month`. eg 20-12-11 satisfies both `year-month-day` and `year-day-month` but is will be parsed as day=11, month=12, year=2020
- This can happen in following two cases:
  - When `DatetimeConfig.year_first=True` and `DatetimeConfig.day_first=None`
  - When `DatetimeConfig` is not provided but regex parsing infers 4 digit year in the beginning. eg 2020-12-11.
- For every other cell in the matrix with multiple formats, only one of the format must satisfy the raw datetime string. If None or more that one format satisfies the datetime string, it is still an ambiguous case.

Consider the examples below:
| `datetime_raw_str` | `year_first` | `day_first` | `result (year-month-day)`|
| ------------------ | -------------| ----------- |---------|
| 01/2/3 04:03:00 | None | None | Couldn't parse |
| 13/02/03 04:03:00 | None | None | Couldn't parse |
| 2021/11/07 04:03:00 | None | None | 2021-11-07T09:03:00Z |
| 2021/32/07 04:03:00 | None | True | Couldn't parse |
| 2021/11/14 04:03:00 | None | True | Couldn't parse |
| 2021/11/07 04:03:00 | None | True | 2021-07-11T08:03:00Z |
| 11\12\2021 04:03:00 | None | True | 2021-12-11T09:03:00Z |
| 01/15/11 04:03:00 | None | True | Couldn't parse |
| 13/02/03 04:03:00 | None | True | 2003-02-13T09:03:00Z |
| 01/02/03 04:03:00 | None | True | 2003-02-01T09:03:00Z |
| 01/02/03 04:03:00 | None | False | Couldn't parse |
| 12/13/03 04:03:00 | None | False | 2003-12-13T09:03:00Z |
| 13-02-03 04:03:00 | None | False | 2013-02-03T09:03:00Z |
| 2021.11.7 04:03:00 | None | False | 2021-11-07T09:03:00Z |
| 2021.11.07 04:03:00.00045000 | None | False | 2021-11-07T09:03:00.00045000Z |
| 01/02/03 04:03:00.0 | True | None | 2001-02-03T09:03:00.0Z |
| 13/02/03 04:03:00 | True | None | 2013-02-03T09:03:00Z |
| 01/02/03 04:03:00 | False | None | Couldn't parse |
| 13/2/03 04:03:00 | False | None | 2003-02-13T09:03:00Z |
| 01/02/03 04:03:00 | True | True | 2001-03-02T09:03:00Z |
| 13/02/03 04:03:00 | True | True | 2013-03-02T09:03:00Z |
| 1/02/03 04:03:00 | True | False | 2001-02-03T09:03:00Z |
| 13/02/03 04:03:00 +05:30 | True | False | 2013-02-02T22:33:00Z |
| 01/15/11 04:03:00 | True | False | Couldn't parse |
| 01/02/03T04:30:00 | False | True | 2003-02-01T09:30:00Z |
| 01/02/3T04:30:00 | False | True | 2003-02-01T09:30:00Z |
| 1/2/3T4:30:00 | False | True | 2003-02-01T09:30:00Z |
| 1/2/3T4:3:00 | False | True | 2003-02-01T09:03:00Z |
| 01/02/13T04:03:00 | False | True | 2013-02-01T09:03:00Z |
| 01/02/03 04:03:00 | False | True | 2003-02-01T09:03:00Z |
| 13/2/03 04:03:00.43500 | False | True | 2003-02-13T09:03:00.43500Z |
| 01/02/03 04:03:00 | False | False | 2003-01-02T09:03:00Z |
| 13/02/3 04:03:00 | False | False | Couldn't parse |
