import pytest
from task_script_utils.datetime_parser import DatetimeConfig, parse
from task_script_utils.datetime_parser.parser_exceptions import DatetimeParserError

four_digit_year_with_no_config_test_cases = [
    # input_, year_first, day_first, expected
    # Unambiguous Cases
    ("2021-12-13T12:12:12 America/Chicago", None, None, "2021-12-13T12:12:12-06:00"),
    ("2021-13-12T12:12:12 America/Chicago", None, None, "2021-12-13T12:12:12-06:00"),
    ("27-12-2002T12:12:12 America/Chicago", None, None, "2002-12-27T12:12:12-06:00"),
    ("27-12-2002T12:12:12Z", None, None, "2002-12-27T12:12:12+00:00"),
    ("2021-13-12T12:12:12Z", None, None, "2021-12-13T12:12:12+00:00"),
    ("12-12-2002T12:12:12 America/Chicago", None, None, "2002-12-12T12:12:12-06:00"),

    # Invalid Cases
    ("32-32-2002T12:12:12 America/Chicago", None, None, None),
    ("32-31-2002T12:12:12 America/Chicago", None, None, None),
    ("27-12-2002 13:12:12 AM America/Chicago", None, None, None),
    ("2021-10-31T02:45:00 Europe/Rome", None, None, None),
    ("2021-23-13T12:12:12 America/Chicago", None, None, None),

    # Ambiguous Case
    ("11-12-2022T12:12:12 America/Chicago", None, None, None),
    ("11-12-22T12:12:12", None, None, None),
    ("2021-12-13T12:12:12 CST", None, None, None)
]

four_digit_year_with_day_first_test_cases = [
    # input_, year_first, day_first, expected
    # Ambiguous cases resolved with datetime config
    ("2021-23-12T12:12:12 America/Chicago", None, True, "2021-12-23T12:12:12-06:00"),
    ("11-12-2002T12:12:12 America/Chicago", None, True, "2002-12-11T12:12:12-06:00"),
    ("2021-12-23T12:12:12 America/Chicago", None, False, "2021-12-23T12:12:12-06:00"),
    ("27-12-2002T12:12:12 America/Chicago", None, True, "2002-12-27T12:12:12-06:00"),
    ("11-12-2002T12:12:12 America/Chicago", None, False, "2002-11-12T12:12:12-06:00"),
    ("2021-12-23T12:12:12Z", None, False, "2021-12-23T12:12:12+00:00"),

    # Note: For short dates with 4 digits year, DatetimeConfig.year_first is ignored
    ("2021/02/3 04:03:00", False, True, "2021-03-02T04:03:00"),
    ("3/02/2021 04:03:00", True, True, "2021-02-03T04:03:00"),

    # Error Cases
    ("2021-12-13T12:12:12 America/Chicago", None, True, None),
    ("2021-13-12T12:12:12 America/Chicago", None, False, None),
    ("2021-12-32T12:12:12 America/Chicago", None, False, None),
    ("13-12-2002T12:12:12 America/Chicago", None, False, None),
    ("12-32-2002T12:12:12 America/Chicago", None, False, None),
]


two_digits_date_cases_with_year_first = [
    # Ambiguous cases resolved with datetime config
    # input_, year_first, day_first, expected
    ("12-12-13T12:12:12Z", True, None, "2012-12-13T12:12:12+00:00"),
    ("21-11-12T12:12:12Z", True, None, "2021-11-12T12:12:12+00:00"),
    ("21-11-12T12:12:12Z", False, None, "2012-11-21T12:12:12+00:00"),
    ("12-13-12T12:12:12Z", True, None, "2012-12-13T12:12:12+00:00"),

    # Still Ambiguous Case
    ("12-11-12T12:12:12Z", False, None, None),
]

two_digits_date_cases_with_day_first = [
    # Ambiguous cases resolved with datetime config
    # input_, year_first, day_first, expected
    ("22-12-13T12:12:12Z", None, True, "2013-12-22T12:12:12+00:00"),
    ("22-12-13T12:12:12Z", None, False, "2022-12-13T12:12:12+00:00"),

    # Still Ambiguous Cases
    ("11-11-13T12:12:12Z", None, False, None)
]

two_digits_date_cases_with_day_first_and_year_first = [
    # Ambiguous cases resolved with datetime config
    # input_, year_first, day_first, expected
    ("22-12-13T12:12:12Z", True, True, "2013-12-22T12:12:12+00:00"), #YY-MM-DD
    ("12-12-13T12:12:12Z", False, False, "2013-12-12:12:12+00:00"), #MM-DD-YY
    ("22-12-13T12:12:12Z", True, False, "2022-12-13T12:12:12+00:00"), #YY-MM-DD
    ("22-12-13T12:12:12Z", False, True, "2013-12-22:12:12+00:00"), #DD-MM-YY

]

parse_test_cases = {
    *four_digit_year_with_no_config_test_cases,
    *four_digit_year_with_day_first_test_cases,
    *two_digits_date_cases_with_year_first,
    *two_digits_date_cases_with_day_first
}

@pytest.mark.parametrize(
    "input_, year_first, day_first, expected",
    parse_test_cases
)
def test_parse(input_, year_first, day_first, expected):
    datetime_config = DatetimeConfig(
        year_first=year_first,
        day_first=day_first
    )
    try:
        parsed_datetime = parse(
            datetime_raw_str=input_,
            config=datetime_config,
        )
        parsed_datetime = parsed_datetime.isoformat()
    except DatetimeParserError as e:
        parsed_datetime = None

    assert parsed_datetime == expected
