"""
A collection of useful functions to parse raw values into a more useable form
"""

from typing import Union, Optional
from decimal import Decimal


class UnparseableValueException(Exception):
    """Represents an error due to trying to parse a value which cannot be parsed"""


def to_int(value: str, strict: bool = False) -> Optional[int]:
    """Converts given value to its equivalent integer.

    :param value: A string to convert
    :type value: string
    :param strict: If set to True, unparsable values raise an exception.
        Default is False, which returns None for unparseable values.
    :return: The int value of the input string or None if the string could not be parsed to int,
        and `strict` is set to False

    """
    # --- Reference implementation ---
    # try:
    #     return int(value)
    # except ValueError as e:
    #     raise UnparseableValueException(f'Could not parse "{value}" to int') from e
    raise NotImplementedError("Not implemented yet")


def to_float(value: str, strict: bool = False) -> Optional[float]:
    """Converts given value to its equivalent float.

    :param value: A string to convert
    :type value: string
    :return: The float value of the input string. None if the string could not be parsed to float
    :raises UnparseableValue: If strict is set to True and the value cannot be parsed
    """
    raise NotImplementedError("Not implemented yet")


def to_number(
    value: Union[str, int, float], strict: bool = False
) -> Union[int, float, None]:
    """Converts the given value to its equivalent number form.
    If the value is already a number, that number is returned.

    :param value: The value to convert
    :type value: string, int, or float
    :return: If the value is already a number, returns it.
        If it is a string, it will return the parsed value of the string.
        If the string cannot be parsed to a number, returns None
    :raises UnparseableValue: If strict is set to True and the value cannot be parsed
    """
    raise NotImplementedError("Not implemented yet")


def to_decimal(value: str, strict: bool = False) -> Optional[Decimal]:
    """Converts the given value to its equivalent python Decimal type

    :param value: The value to convert
    :type value: string
    :return: The decimal value of the input string.  None if the string could not be converted to Decimal
    :raises UnparseableValue: If strict is set to True and the value cannot be parsed
    """
    raise NotImplementedError("Not implemented yet")


def to_boolean(value: str, strict: bool = False) -> Optional[bool]:
    """Converts given value to its equivalent boolean.

    :param value: A string to convert
    :type value: string
    :return: The boolean value of the input string.
        None if the string could not be parsed to boolean
    :raises UnparseableValue: If strict is set to True and the value cannot be parsed
    """
    raise NotImplementedError("Not implemented yet")
