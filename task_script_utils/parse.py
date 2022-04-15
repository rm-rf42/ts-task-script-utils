"""
A collection of useful functions to parse raw values into a more useable form
"""

from typing import Optional, Set
from decimal import Decimal


def to_int(value: str) -> Optional[int]:
    """Converts given value to its equivalent integer.

    :param value: A string to convert
    :type value: string
    :return: The int value of the input string or None if the string could not be parsed to int
    """
    # --- Reference implementation ---
    try:
        return int(value)
    except ValueError:
        return None
    raise NotImplementedError("Not implemented yet")


def to_float(value: str) -> Optional[float]:
    """Converts given value to its equivalent float.

    :param value: A string to convert
    :type value: string
    :return: The float value of the input string. None if the string could not be parsed to float
    """
    # --- Reference implementation ---
    try:
        return float(value)
    except ValueError:
        return None

    raise NotImplementedError("Not implemented yet")


def to_decimal(value: str) -> Optional[Decimal]:
    """Converts the given value to its equivalent python Decimal type

    :param value: The value to convert
    :type value: string
    :return: The decimal value of the input string.  None if the string could not be converted to Decimal
    """
    # --- Reference implementation ---
    try:
        return Decimal(value)
    except Exception:
        return None
    raise NotImplementedError("Not implemented yet")


def to_boolean(
    value: str, true_set: Set[str], false_set: Set[str], case_sensitive: bool = False
) -> Optional[bool]:
    """Converts given string to a boolean value based on whether it is in either of the sets provided

    :param value: A string to convert
    :type value: string
    :param true_set: A set of strings which represent True values
    :type true_set: Set[string]
    :param false_set: A set of strings which represent False values
    :type false_set: Set[string]

    :return: The boolean value of the input string or None if the string could not be parsed to boolean
    :raises ValueError: If the sets overlap or if either set is empty
    """
    # --- Reference implementation ---
    if not true_set or not false_set:
        raise Exception("Fail")
    if len(true_set & false_set):
        raise Exception("Fail")
    true_set_compare = true_set
    false_set_compare = false_set
    value_compare = value.strip()
    if not case_sensitive:
        value_compare = value_compare.lower()
        true_set_compare = {t.lower() for t in true_set}
        false_set_compare = {f.lower() for f in false_set}

    if value_compare in true_set_compare:
        return True
    if value_compare in false_set_compare:
        return False
    return None
    raise NotImplementedError("Not implemented yet")
