"""
Test `to_decimal()` function in parse.py

We use `compare_total()` because it compares the exact decimal representation, not just numeric equality

For example:

>>> Decimal("12.34").compare_total(Decimal("12.34"))
Decimal('0')
>>> Decimal("12.34").compare_total(Decimal("1234e-2"))
Decimal('0')

>>> Decimal("12.34").compare_total(Decimal("12.3400"))
Decimal('1')
"""
from decimal import Decimal
import pytest
from task_script_utils import parse


def test_to_decimal_positive_integer():
    """Test Positive Integer."""
    # Arrange
    value = "2022"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("2022")) == 0


def test_to_decimal_positive_decimal():
    """Test Positive decimal."""
    # Arrange
    value = "32.5"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("32.5")) == 0


def test_to_decimal_positive_integer_with_plus():
    """Test Positive integer with +."""
    # Arrange
    value = "+1024"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("1024")) == 0


def test_to_decimal_positive_decimal_with_plus():
    """Test Positive decimal with +."""
    # Arrange
    value = "+99.99"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("99.99")) == 0


def test_to_decimal_negative_integer():
    """Test Negative integer."""
    # Arrange
    value = "-40"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-40")) == 0


def test_to_decimal_negative_decimal():
    """Test Negative decimal."""
    # Arrange
    value = "-67.1322"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-67.1322")) == 0


def test_to_decimal_decimal_with_trailing_zeros():
    """Test Decimal with trailing zeros."""
    # Arrange
    value = "12.3400"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("12.3400")) == 0


def test_to_decimal_negative_decimal_with_trailing_zeros():
    """Test Negative decimal with trailing zeros."""
    # Arrange
    value = "-56.78000"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-56.78000")) == 0


def test_to_decimal_zero():
    """Test Zero."""
    # Arrange
    value = "0"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("0")) == 0


def test_to_decimal_positive_zero():
    """Test Positive Zero."""
    # Arrange
    value = "+0"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("0")) == 0


def test_to_decimal_negative_zero():
    """Test Negative Zero."""
    # Arrange
    value = "-0"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-0")) == 0


def test_to_decimal_zero_with_a_side_of_extra_zeros():
    """Test Zero with a side of extra Zeros."""
    # Arrange
    value = "0.0000000"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("0.0000000")) == 0


def test_to_decimal_scientific_notation():
    """Test Scientific Notation."""
    # Arrange
    value = "2.99e8"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("2.99E+8")) == 0


def test_to_decimal_scientific_notation_negative_exponent():
    """Test Scientific Notation, negative exponent."""
    # Arrange
    value = "3.14e-3"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("0.00314")) == 0


def test_to_decimal_negative_scientific_notation():
    """Test Scientific Notation."""
    # Arrange
    value = "-5e5"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-5E+5")) == 0


def test_to_decimal_negative_scientific_notation_negative_exponent():
    """Test Scientific Notation, negative exponent."""
    # Arrange
    value = "-2.74e-3"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-0.00274")) == 0


def test_to_decimal_scientific_notation_negative_exponent_greater_than_1():
    """Test Scientific Notation, negative exponent, greater than 1."""
    # Arrange
    value = "1000e-2"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("10.00")) == 0


@pytest.mark.parametrize("value", ["  \t  128.01", "128.01       ", "\t128.01\t \t "])
def test_to_decimal_whitespace(value):
    """Test whitespace."""
    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("128.01")) == 0


def test_to_decimal_decimal_representation_of_integer():
    """Test Decimal representation of integer."""
    # Arrange
    value = "512.00"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("512.00")) == 0


def test_to_decimal_decimal_representation_of_negative_integer():
    """Test Decimal representation of integer."""
    # Arrange
    value = "-512.00"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert isinstance(actual, Decimal)
    assert actual.compare_total(Decimal("-512.00")) == 0


def test_to_decimal_string_has_underscores_integer():
    """Test String has underscores (integer)."""
    # Arrange
    value = "20_48"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual is None


def test_to_decimal_string_has_underscores_decimal():
    """Test String has underscores (decimal)."""
    # Arrange
    value = "1_499_999.9_9"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual is None


def test_to_decimal_very_large_float():
    """Test a very large in positive value is parsed correctly."""
    # Arrange
    value = "114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376.0"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert (
        actual.compare_total(
            Decimal(
                "114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376.0"
            )
        )
        == 0
    )


def test_to_decimal_very_large_negative_float():
    """Test a very large in magnitude negative value is parsed correctly."""
    # Arrange
    value = "-114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376.0"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert (
        actual.compare_total(
            Decimal(
                "-114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376.0"
            )
        )
        == 0
    )


def test_to_decimal_very_small_positive_number():
    """Test a very small positive value is parsed correctly."""
    # Arrange
    value = "0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert (
        actual.compare_total(
            Decimal(
                "0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            )
        )
        == 0
    )


def test_to_decimal_very_small_negative_number():
    """Test a very small negative value is parsed correctly."""
    # Arrange
    value = "-0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert (
        actual.compare_total(
            Decimal(
                "-0.00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001"
            )
        )
        == 0
    )


@pytest.mark.parametrize(
    "value",
    [
        "nan",
        "NaN",
        "NAN",
    ],
)
def test_to_decimal_nan_strings(value):
    """Test not a number strings."""
    # Arrange from parameters
    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual.is_nan()


def test_to_decimal_positive_infinity():
    """Test positive infinity is parsed into a positive infinity value."""
    # Arrange
    value = "inf"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual.is_infinite()
    assert actual > 0


def test_to_decimal_negative_infinity():
    """Test negative infinity is parsed into a negative infinity value."""
    # Arrange
    value = "-inf"

    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual.is_infinite()
    assert actual < 0


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
        "infinity",
        "INFINITY",
        "-infinity",
        "-INFINITY",
    ],
)
def test_to_decimal_invalid_strings(value):
    """Test Invalid strings."""
    # Arrange from parameters
    # Act
    actual = parse.to_decimal(value)

    # Assert
    assert actual is None
