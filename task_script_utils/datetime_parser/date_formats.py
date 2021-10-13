from itertools import product

date_parts = [
    ['dddd', 'ddd ', 'dddd, ', 'ddd, ', ''],
    ['MMMM', 'MMM'],
    ['Do,', 'Do', 'D,', 'D'],
    ['YYYY']
]

long_date_formats = product(*date_parts)
long_date_formats = [
    " ".join(tokens).strip().replace("  ", " ")
    for tokens in long_date_formats
]
