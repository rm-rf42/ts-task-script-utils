"""Test `to_boolean()` function in parse.py."""
import pytest
from task_script_utils import parse


@pytest.mark.parametrize("value", ["True", "False", "Something else"])
@pytest.mark.parametrize("case_sensitive", [True, False])
def test_to_boolean_empty_sets(value, case_sensitive):
    """Test Empty Sets."""
    # Arrange

    # Act

    # Assert
    with pytest.raises(Exception):
        parse.to_boolean(value, set(), set(), case_sensitive=case_sensitive)


@pytest.mark.parametrize("value", ["True", "False", "Something else"])
@pytest.mark.parametrize("case_sensitive", [True, False])
def test_to_boolean_empty_true_set(value, case_sensitive):
    """Test Empty True Set."""
    # Arrange

    # Act

    # Assert
    with pytest.raises(Exception):
        parse.to_boolean(value, set(), {"False"}, case_sensitive=case_sensitive)


@pytest.mark.parametrize("value", ["True", "False", "Something else"])
@pytest.mark.parametrize("case_sensitive", [True, False])
def test_to_boolean_empty_false_set(value, case_sensitive):
    """Test Empty False Set."""
    # Arrange

    # Act

    # Assert
    with pytest.raises(Exception):
        parse.to_boolean(
            value, {"true", "1", "yes"}, set(), case_sensitive=case_sensitive
        )


@pytest.mark.parametrize("value", ["True", "1", "yes"])
def test_to_boolean_case_sensitive_string_is_in_true_set(value):
    """Test Case sensitive string is in True Set."""
    # Arrange
    case_sensitive = True

    # Act

    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is True


@pytest.mark.parametrize(
    "value", ["yes", "Yes", "yEs", "yeS", "YEs", "YeS", "yES", "YES"]
)
def test_to_boolean_case_insensitive_string_is_in_true_set(value):
    """Test Case insensitive string is in True Set."""
    # Arrange
    case_sensitive = False

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is True


@pytest.mark.parametrize("value", ["False", "0", "no"])
def test_to_boolean_case_sensitive_string_is_in_false_set(value):
    """Test Case sensitive string is in False Set."""
    # Arrange
    case_sensitive = True

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is False


@pytest.mark.parametrize("value", ["no", "No", "nO", "NO"])
def test_to_boolean_case_insensitive_string_is_in_false_set(value):
    """Test Case insensitive string is in False Set."""
    # Arrange
    case_sensitive = False

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is False


@pytest.mark.parametrize(
    "value",
    ["TRUE", "FALSE", "Yes", "yEs", "yeS", "YEs", "YeS", 'yES""YES', "No", "nO", "NO"],
)
def test_to_boolean_case_sensitive_string_is_not_in_either_set_but_looks_like_it_should_be(
    value,
):
    """Test Case sensitive string is not in either set, but looks like it should be."""
    # Arrange
    case_sensitive = True

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is None


@pytest.mark.parametrize("value", ["    True", " 1", "\\t   \\t yes"])
def test_to_boolean_leading_whitespace_true_(value):
    """Test Leading whitespace (true)."""
    # Arrange
    case_sensitive = True

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is True


@pytest.mark.parametrize("value", ["True   ", "1\\t", "yes     \\t\\t"])
def test_to_boolean_trailing_whitespace_true_(value):
    """Test Trailing whitespace (true)."""
    # Arrange
    case_sensitive = True

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is True


@pytest.mark.parametrize("value", ["     False ", "\\t\\t0\\t\\t", "  no\\t  "])
def test_to_boolean_surrounding_whitespace(value):
    """Test Surrounding whitespace."""
    # Arrange
    case_sensitive = True

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is False


@pytest.mark.parametrize(
    "value",
    [
        "I’m pretty confident this is true",
        "null",
        "",
        "00",
        "01",
        "10",
        "TrueFalse",
        "True False",
        "-",
        "    ",
        "Τʀυe",
    ],
)
@pytest.mark.parametrize("case_sensitive", [True, False])
def test_to_boolean_string_is_not_in_either_set(value, case_sensitive):
    """Test String is not in either set."""
    # Arrange

    # Act
    actual = parse.to_boolean(
        value, {"True", "1", "yes"}, {"False", "0", "no"}, case_sensitive=case_sensitive
    )

    # Assert
    assert actual is None
