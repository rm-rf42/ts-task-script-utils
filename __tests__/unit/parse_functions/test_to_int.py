"""
Test `to_int()` function in parse.py
"""
from task_script_utils import parse
import pytest


def test_to_int_positive_integer():
    """Test Positive Integer"""
    value = "2022"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 2022


def test_to_int_positive_integer_with_plus():
    """Test Positive integer with +"""
    value = "+1024"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 1024


def test_to_int_negative_integer():
    """Test Negative integer"""
    value = "-40"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == -40


def test_to_int_zero():
    """Test Zero"""
    value = "0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 0


def test_to_int_positive_zero():
    """Test Positive Zero"""
    value = "+0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 0


def test_to_int_negative_zero():
    """Test Negative Zero"""
    value = "-0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 0


def test_to_int_scientific_notation():
    """Test Scientific Notation"""
    value = "2.99e8"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 299000000


@pytest.mark.parametrize("value", ["3.14e-3", "2718e-3"])
def test_to_int_scientific_notation__negative_exponent__between_0_and_1(value):

    """Test Scientific Notation, negative exponent, between 0 and 1"""
    # Arrange from parameters

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


@pytest.mark.parametrize("value", ["3.14e-3", "2718e-3"])
def test_to_int_scientific_notation__negative_exponent__between_0_and_1(value):

    """Test Scientific Notation, negative exponent, between 0 and 1"""
    # Arrange from parameters

    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)


def test_to_int_scientific_notation__negative_exponent__greater_than_1():
    """Test Scientific Notation, negative exponent, greater than 1"""
    value = "1000e-2"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_scientific_notation__negative_exponent__greater_than_1():
    """Test Scientific Notation, negative exponent, greater than 1"""
    value = "1000e-2"
    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)


def test_to_int_scientific_notation():
    """Test Scientific Notation"""
    value = "-5e5"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == -500000


def test_to_int_scientific_notation__negative_exponent():
    """Test Scientific Notation, negative exponent"""
    value = "-2.74e-3"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_scientific_notation__negative_exponent():
    """Test Scientific Notation, negative exponent"""
    value = "-2.74e-3"
    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)


def test_to_int_leading_whitespace():
    """Test Leading whitespace"""
    value = "  \t  64"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 64


def test_to_int_trailing_whitespace():
    """Test Trailing whitespace"""
    value = "128       "

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 128


def test_to_int_surrounding_whitespace():
    """Test Surrounding whitespace"""
    value = "\t256\t \t "

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 256


def test_to_int_decimal():
    """Test Decimal"""
    value = "3.1415"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_decimal():
    """Test Decimal"""
    value = "3.1415"
    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)


def test_to_int_decimal_representation_of_integer():
    """Test Decimal representation of integer"""
    value = "512.00"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_decimal_representation_of_integer():
    """Test Decimal representation of integer"""
    value = "512.00"
    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)


def test_to_int_string_has_underscores():
    """Test String has underscores"""
    value = "20_48"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual == 2048


@pytest.mark.parametrize(
    "value",
    [
        "two",
        "12.4.5",
        "1/2",
        "4 + 2i",
        "5 + 3j",
        "2,500",
        "0xbadbeef",
        "0o775",
        "0b100001",
    ],
)
def test_to_int_invalid_strings(value):
    """Test Invalid strings"""
    # Arrange from parameters

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


@pytest.mark.parametrize(
    "value",
    [
        "two",
        "12.4.5",
        "1/2",
        "4 + 2i",
        "5 + 3j",
        "2,500",
        "0xbadbeef",
        "0o775",
        "0b100001",
    ],
)
def test_to_int_invalid_strings(value):
    """Test Invalid strings"""
    # Arrange from parameters

    # Act + Assert
    with pytest.raises(parse.UnparseableValueException):
        parse.to_int(value, strict=True)
