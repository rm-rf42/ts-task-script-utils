from itertools import product

from pydash.arrays import flatten

date_parts = [
    ['dddd', 'ddd', 'dddd,', 'ddd,', ''],
    ['MMMM', 'MMM'],
    ['Do,', 'Do', 'D,', 'D'],
    ['YYYY']
]

time_parts = [
    ["h", "hh", "H", "HH"],
    ["m", "mm"],
    ["s", "ss"],
]

long_date_formats = product(*date_parts)
long_date_formats = [
    " ".join(tokens).strip()
    for tokens in long_date_formats
]


def get_time_formats():
    def map_am_pm(time_format):
        return (
            time_format
            if time_format.startswith("H")
            else time_format + " A"
        )

    time_formats = [
        ":".join(tokens)
        for tokens in product(*time_parts)
    ]
    time_formats = map(lambda x: [x, x+".SSS"], time_formats)
    time_formats = flatten(time_formats)
    time_formats = map(lambda x: map_am_pm(x), time_formats)
    time_formats = map(
        lambda x: [
            x,
            x + " Z",
            x + " z",
            x + " ZZ",
            x + " Z z",
            x + " ZZ z"],
        time_formats
    )
    time_formats = flatten(time_formats)
    return time_formats


def get_long_datetime_formats():
    parts = [long_date_formats, get_time_formats()]
    formats = [
        " ".join(values)
        for values in product(*parts)
    ]
    return formats
