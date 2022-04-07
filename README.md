# ts-task-script-utils <!-- omit in toc -->

[![Build Status](https://travis-ci.com/tetrascience/ts-task-script-utils.svg?branch=master)](https://travis-ci.com/tetrascience/ts-task-script-utils)

Utility functions for Tetra Task Scripts

- [Installation](#installation)
- [Usage](#usage)
- [Datetime Parser](#datetime-parser)
- [Test](#test)
- [Changelog](#changelog)
  - [v1.2.0](#v120)
  - [v1.1.1](#v111)
  - [v1.1.0](#v110)
## Installation

`pip install ts-task-script-utils`

## Usage

`from task_script_utils.is_number import isnumber`

`print(isnumber('a'))`

## Datetime Parser

```python
from task_script_utils.datetime_parser import parse

parse("2004-12-23T12:30 AM +05:30")
parse("2004-12-23T12:30 AM +05:30", <datetime_config>)
parse("2004-12-23T12:30 AM +05:30", <format_list>)
parse("2004-12-23T12:30 AM +05:30", <format_list>, <datetime_config>)
```

`parse()` returns a `TSDatetime` Object. You can use `TSDatetime.tsformat()` and
`TSDatetime.isoformat()` to get datetime string. You can also use
`TSDatetime.datetime()` to access python datetime object.

You can read more about the datetime parser [here](task_script_utils/datetime_parser/README.md).

## Test

`pipenv install --dev`
then
`pipenv run python -m pytest`

## Changelog

### v1.2.0

- Add boolean config parameter `require_unambiguous_formats` to `DatetimeConfig`
- Add logic to `parser._parse_with_formats` to be used when `DatetimeConfig.require_unambiguous_formats` is set to `True`
  - `AmbiguousDatetimeFormatsError` is raised if mutually ambiguous formats are detected and differing datetimes are parsed
- Add parameter typing throughout repository
- Refactor `datetime_parser` package
- Add base class `DateTimeInfo`
- Segregate parsing logic into `ShortDateTimeInfo` and `LongDateTimeInfo`

### v1.1.1

- Remove `convert_to_ts_iso8601()` method

### v1.1.0

- Add `datetime_parser` package
