"""
Test `to_int()` function in parse.py
"""
import pytest
from task_script_utils import parse


def test_to_int_positive_integer():
    """Test Positive Integer."""
    # Arrange
    value = "2022"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 2022


def test_to_int_positive_integer_with_plus():
    """Test Positive integer with +."""
    # Arrange
    value = "+1024"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 1024


def test_to_int_negative_integer():
    """Test Negative integer."""
    # Arrange
    value = "-40"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == -40


def test_to_int_zero():
    """Test Zero."""
    # Arrange
    value = "0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 0


def test_to_int_positive_zero():
    """Test Positive Zero."""
    # Arrange
    value = "+0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 0


def test_to_int_negative_zero():
    """Test Negative Zero."""
    # Arrange
    value = "-0"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 0


def test_to_int_scientific_notation():
    """Test Scientific Notation."""
    # Arrange
    value = "2.99e8"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 299000000


@pytest.mark.parametrize("value", ["3.14e-3", "2718e-3"])
def test_to_int_scientific_notation_negative_exponent_between_0_and_1(value):
    """Test Scientific Notation, negative exponent, between 0 and 1."""
    # Arrange from parameters
    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_scientific_notation_negative_exponent_greater_than_1():
    """Test Scientific Notation, negative exponent, greater than 1."""
    # Arrange
    value = "1000e-2"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 10


def test_to_int_negative_scientific_notation():
    """Test Scientific Notation."""
    # Arrange
    value = "-5e5"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == -500000


def test_to_int_scientific_notation_negative_exponent():
    """Test Scientific Notation, negative exponent."""
    # Arrange
    value = "-2.74e-3"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_leading_whitespace():
    """Test Leading whitespace."""
    # Arrange
    value = "  \t  64"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 64


def test_to_int_trailing_whitespace():
    """Test Trailing whitespace."""
    # Arrange
    value = "128       "

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 128


def test_to_int_surrounding_whitespace():
    """Test Surrounding whitespace."""
    # Arrange
    value = "\t256\t \t "

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 256


def test_to_int_decimal():
    """Test Decimal."""
    # Arrange
    value = "3.1415"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_decimal_representation_of_integer():
    """Test Decimal representation of integer."""
    # Arrange
    value = "512.00"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 512


def test_to_int_string_has_underscores():
    """Test String has underscores."""
    # Arrange
    value = "20_48"

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
    """Test Invalid strings."""
    # Arrange from parameters
    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None
