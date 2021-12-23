# ts-task-script-utils <!-- omit in toc -->

[![Build Status](https://travis-ci.com/tetrascience/ts-task-script-utils.svg?branch=master)](https://travis-ci.com/tetrascience/ts-task-script-utils)

Utility functions for Tetra Task Scripts

- [Installation](#installation)
- [Usage](#usage)
- [Datetime Parser](#datetime-parser)
  - [Usage](#usage-1)
  - [DatetimeConfig](#datetimeconfig)
  - [Datetime format resolution matrix](#datetime-format-resolution-matrix)
  - [Format Tokens](#format-tokens)
  - [Limitations](#limitations)
- [Test](#test)

## Installation

`pip install ts-task-script-utils`

## Usage

`from task_script_utils.is_number import isnumber`

`print(isnumber('a'))`

## Datetime Parser

### Usage

```python
from task_script_utils.datetime_parser import convert_to_ts_iso8601

convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30")
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <datetime_config>)
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <format_list>)
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <format_list>, <datetime_config>)
```

### DatetimeConfig

DatetimeConfig is used to provide complementary information that helps
to parse datetime

```python
from task_script_utils.datetime_parser import DatetimeConfig
```

A `DatetimeConfig` object has following attributes:

- `day_first: Optional[bool]`: `True/False`. Defaults to `None`
  - Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the day (True) or month (False).
- `year_first: Optional[bool]`: `True/False`. Defaults to `None`
  - Whether to interpret the first value in an ambiguous 3-integer date (e.g. 01/05/09) as the year.  When the year is specified in four digits, this configuration is ignored.
- `tz_dict: Optional[dict]`: a `dict` mapping abbreviated_tz to offset value. Defaults to `empty dict`.

```python
  sample_tz_dict = {
      "IST": "+05:30",
      "EST": "-05:00",
      "CST": "-06:00",
  }

  # Inbuilt tz_dict
  from task_script_utils.datetime_parser.tz_dicts import USA
  print(USA)
  {
    "EDT": "-04:00",
    "EST": "-05:00",
    "CDT": "-05:00",
    "CST": "-06:00",
    "MDT": "-06:00",
    "MST": "-07:00",
    "PDT": "-07:00",
    "PST": "-08:00",
  }
```

- `fold: Optional[int]`: `0`, `1`. Defaults to `None`.
  - It is required during the 2 hour window when clocks are set back in a timezone which keeps track of daylight savings (such as IANA timezones like `Europe/London`).
  - The allowed values for the fold attribute will be 0 and 1 with 0 corresponding to the earlier and 1 to the later of the two possible readings of an ambiguous local time.
  - If fold is `None`, Parser will check if `fold` is needed or not to parse the time with no ambiguity.
  - `AmbiguousFoldError` will be raised if `fold` is needed.

### Datetime format resolution

| year_first | day_first | possible formats                                       |
| ---------- | --------- | ------------------------------------------------------ |
| True       | True      | year-day-month                                         |
| True       | False     | year-month-day                                         |
| True       | None      | year-month-day <br> year-day-month                     |
| False      | False     | month-day-year                                         |
| False      | True      | day-month-year                                         |
| False      | None      | month-day-year <br> day-month-year                     |
| None       | True      | day-month-year                                         |
| None       | False     | year-month-day <br> month-day-year                     |
| None       | None      | month-day-year <br> day-month-year <br> year-month-day |

When the year has four digits, then whether `year_first` is `true` or `false`, is decided by regex parsing done by `DatetimeInfo`.
In this case the value of `DatetimeConfig.year_first` is ignored. Only `DatetimeInfo.day_first` is taken into account.

### Format Tokens

`convert_to_ts_iso8601` or `parse` accepts `formats_list: Tuple` as an arguments.
Each format string in `formats_list` must be build using `Pendulum` 's format tokens

The following tokens are currently supported:

|                            | Token  | Output                            |
| -------------------------- | ------ | --------------------------------- |
| **Year**                   | YYYY   | 2000, 2001, 2002 ... 2012, 2013   |
|                            | YY     | 00, 01, 02 ... 12, 13             |
|                            | Y      | 2000, 2001, 2002 ... 2012, 2013   |
| **Quarter**                | Q      | 1 2 3 4                           |
|                            | Qo     | 1st 2nd 3rd 4th                   |
| **Month**                  | MMMM   | January, February, March ...      |
|                            | MMM    | Jan, Feb, Mar ...                 |
|                            | MM     | 01, 02, 03 ... 11, 12             |
|                            | M      | 1, 2, 3 ... 11, 12                |
|                            | Mo     | 1st 2nd ... 11th 12th             |
| **Day of Year**            | DDDD   | 001, 002, 003 ... 364, 365        |
|                            | DDD    | 1, 2, 3 ... 4, 5                  |
| **Day of Month**           | DD     | 01, 02, 03 ... 30, 31             |
|                            | D      | 1, 2, 3 ... 30, 31                |
|                            | Do     | 1st, 2nd, 3rd ... 30th, 31st      |
| **Day of Week**            | dddd   | Monday, Tuesday, Wednesday ...    |
|                            | ddd    | Mon, Tue, Wed ...                 |
|                            | dd     | Mo, Tu, We ...                    |
|                            | d      | 0, 1, 2 ... 6                     |
| **Days of ISO Week**       | E      | 1, 2, 3 ... 7                     |
| **Hour**                   | HH     | 00, 01, 02 ... 23, 24             |
|                            | H      | 0, 1, 2 ... 23, 24                |
|                            | hh     | 01, 02, 03 ... 11, 12             |
|                            | h      | 1, 2, 3 ... 11, 12                |
| **Minute**                 | mm     | 00, 01, 02 ... 58, 59             |
|                            | m      | 0, 1, 2 ... 58, 59                |
| **Second**                 | ss     | 00, 01, 02 ... 58, 59             |
|                            | s      | 0, 1, 2 ... 58, 59                |
| **Fractional Second**      | SSSSSS | All fractional digits             |
| **AM / PM**                | A      | AM, PM                            |
| **Timezone**               | Z      | -07:00, -06:00 ... +06:00, +07:00 |
|                            | ZZ     | -0700, -0600 ... +0600, +0700     |
|                            | z      | Asia/Baku, Europe/Warsaw, GMT ... |
|                            | zz     | EST CST ... MST PST               |
| **Seconds timestamp**      | X      | 1381685817, 1234567890.123        |
| **Milliseconds timestamp** | x      | 1234567890123                     |

**Note: If `zz` token is used in format string, passing `tz_dict` is a must.**

### Limitations

1. It is not possible to parse just dates or just times alone.
   eg.`parse('2021-12-08')` or `parse('2021-12-08')` will raise `InvalidDateError`

## Test

`pipenv install --dev`
then
`pipenv run python -m pytest`
