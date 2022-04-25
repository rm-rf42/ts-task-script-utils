"""Test `to_int()` function in parse.py."""
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


@pytest.mark.parametrize(
    "value",
    ["1e0", "1e+0", "1e-0", "1.0e0", "1.0e+0", "1.0e-0"],
)
def test_to_int_scientific_notation_zero_exponent(value):
    """Test Scientific Notation, zero exponent."""
    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int)
    assert actual == 1


@pytest.mark.parametrize("value", ["  \t  128", "128       ", "\t128\t \t "])
def test_to_int_whitespace(value):
    """Test whitespace."""
    # Act
    actual = parse.to_int(value)

    # Assert
    assert isinstance(actual, int), f"Expected int, got {actual} ({type(actual)})"
    assert actual == 128


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


def test_to_int_very_large():
    """Test a very large in positive value is parsed correctly."""
    # Arrange
    value = "114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert (
        actual
        == 114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376
    )


def test_to_int_very_large_negative():
    """Test a very large in magnitude negative value is parsed correctly."""
    # Arrange
    value = "-114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert (
        actual
        == -114813069527425452423283320117768198402231770208869520047764273682576626139237031385665948631650626991844596463898746277344711896086305533142593135616665318539129989145312280000688779148240044871428926990063486244781615463646388363947317026040466353970904996558162398808944629605623311649536164221970332681344168908984458505602379484807914058900934776500429002716706625830522008132236281291761267883317206598995396418127021779858404042159853183251540889433902091920554957783589672039160081957216630582755380425583726015528348786419432054508915275783882625175435528800822842770817965453762184851149029376
    )


@pytest.mark.parametrize(
    "value",
    [
        "nan",
        "NaN",
        "NAN",
    ],
)
def test_to_int_nan_strings(value):
    """Test not a number strings."""
    # Arrange from parameters
    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_positive_infinity():
    """Test positive infinity is parsed to None (i.e. considered invalid input)."""
    # Arrange
    value = "inf"

    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None


def test_to_int_negative_infinity():
    """Test negative infinity is parsed to None (i.e. considered invalid input)."""
    # Arrange
    value = "-inf"

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
        "infinity",
        "INFINITY",
        "-infinity",
        "-INFINITY",
    ],
)
def test_to_int_invalid_strings(value):
    """Test Invalid strings."""
    # Arrange from parameters
    # Act
    actual = parse.to_int(value)

    # Assert
    assert actual is None
