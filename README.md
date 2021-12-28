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

```python
from task_script_utils.datetime_parser import convert_to_ts_iso8601

convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30")
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <datetime_config>)
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <format_list>)
convert_to_ts_iso8601("2004-12-23T12:30 AM +05:30", <format_list>, <datetime_config>)
```

You can read more about the datetime parser [here.](spec.md)

## Test

`pipenv install --dev`
then
`pipenv run python -m pytest`
