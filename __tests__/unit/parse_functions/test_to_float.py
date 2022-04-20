"""
Test `to_float()` function in parse.py
"""
import pytest
from task_script_utils import parse


def test_to_float_positive_integer():
    """Test Positive Integer"""
    # Arrange
    value = "2022"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 2022.0


def test_to_float_positive_decimal():
    """Test Positive decimal"""
    # Arrange
    value = "32.23"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 32.23


def test_to_float_positive_integer_with_plus():
    """Test Positive integer with +"""
    # Arrange
    value = "+1024"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 1024.0


def test_to_float_positive_decimal_with_plus():
    """Test Positive decimal with +"""
    # Arrange
    value = "+99.99"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 99.99


def test_to_float_negative_integer():
    """Test Negative integer"""
    # Arrange
    value = "-40"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == -40.0


def test_to_float_negative_decimal():
    """Test Negative decimal"""
    # Arrange
    value = "-67.1322"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == -67.1322


def test_to_float_decimal_with_trailing_zeros():
    """Test Decimal with trailing zeros"""
    # Arrange
    value = "12.340000000"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 12.34


def test_to_float_negative_decimal_with_trailing_zeros():
    """Test Negative decimal with trailing zeros"""
    # Arrange
    value = "-56.78000"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == -56.78


def test_to_float_zero():
    """Test Zero"""
    # Arrange
    value = "0"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 0.0


def test_to_float_positive_zero():
    """Test Positive Zero"""
    # Arrange
    value = "+0"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 0.0


def test_to_float_negative_zero():
    """Test Negative Zero"""
    # Arrange
    value = "-0"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 0.0


def test_to_float_zero_with_a_side_of_extra_zeros():
    """Test Zero with a side of extra Zeros"""
    # Arrange
    value = "0.0000000"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 0.0


def test_to_float_scientific_notation():
    """Test Scientific Notation"""
    # Arrange
    value = "2.99e8"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 299000000.0


def test_to_float_scientific_notation_negative_exponent():
    """Test Scientific Notation, negative exponent"""
    # Arrange
    value = "3.14e-3"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 0.00314


def test_to_float_negative_scientific_notation():
    """Test Scientific Notation"""
    # Arrange
    value = "-5e5"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == -500000.0


def test_to_float_negative_scientific_notation_negative_exponent():
    """Test Scientific Notation, negative exponent"""
    # Arrange
    value = "-2.74e-3"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == -0.00274


def test_to_float_scientific_notation_negative_exponent_greater_than_1():
    """Test Scientific Notation, negative exponent, greater than 1"""
    # Arrange
    value = "1000e-2"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 10.0


def test_to_float_leading_whitespace():
    """Test Leading whitespace"""
    # Arrange
    value = "  \t  64.01"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 64.01


def test_to_float_trailing_whitespace():
    """Test Trailing whitespace"""
    # Arrange
    value = "128.28       "

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 128.28


def test_to_float_surrounding_whitespace():
    """Test Surrounding whitespace"""
    # Arrange
    value = "\t256.99\t \t "

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 256.99


def test_to_float_decimal_representation_of_integer():
    """Test Decimal representation of integer"""
    # Arrange
    value = "512.00"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert isinstance(actual, float), f"Expected float, got {actual} ({type(actual)})"
    assert actual == 512.0


def test_to_float_string_has_underscores_integer():
    """Test String has underscores (integer)"""
    # Arrange
    value = "20_48"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert actual is None


def test_to_float_string_has_underscores_decimal():
    """Test String has underscores (decimal)"""
    # Arrange
    value = "1_499_999.9_9"

    # Act
    actual = parse.to_float(value)

    # Assert
    assert actual is None


@pytest.mark.parametrize(
    "value",
    [
        "two",
        "thirty-five point seven",
        "12.4.5",
        "1/2",
        "4 + 2i",
        "5.2 - 3.7j",
        "2,500",
        "0xbadbeef",
        "0o775",
        "0b100001",
    ],
)
def test_to_float_invalid_strings(value):
    """Test Invalid strings"""
    # Arrange from parameters
    # Act
    actual = parse.to_float(value)

    # Assert
    assert actual is None
