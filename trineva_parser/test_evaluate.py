import pytest
from helpers import *

@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("2 + 2", 4),
        ("-5 + 10", 5),
        ("10 - 15", -5),
        ("4 * 4", 16),
        ("20 / 5", 4.0),
        ("5 + 3 * 2", 11),
        ("(5 + 5) * 2", 20),
        ("// comment // 5 + 3 // comment //", 8),
        ("5 // some comment // - 2", 3),
        ("(4 + 6) // comment // * 2", 20),
        ("x = 5; y = 3; x + y", 8),
        ("a = 10; b = 20; a * b", 200),
        ("x = 5; y = x * 2; z = y + 3; z", 13),
        ("x = -5; y = x * 2; z = y + 3; z", -7),
        ("a = 10; b = 5; c = a / b; c + 2", 4.0),
        ("var1 = 4; var2 = 6; (var1 + var2) * 2", 20),
        ("x = 2 + 3; y = x * 4; y + 1", 21),
    ]
)
def test_valid_expressions(expression, expected_result):
    assert evaluate(expression) == expected_result


@pytest.mark.parametrize(
    "expression, expected_exception, error_message",
    [
        ("5 +", InvalidExpressionException, ERROR_INVALID_STRUCTURE),
        ("(5 + 3", InvalidExpressionException, ERROR_MISMATCHED_PARENTHESES),
        ("5 + 3)", InvalidExpressionException, ERROR_MISMATCHED_PARENTHESES),
        ("10 / 0", InvalidExpressionException, ERROR_DIVISION_BY_ZERO),
        ("5 + 3 & 2", InvalidExpressionException, ERROR_INVALID_OPERATOR.format("&")),
        ("// only comment //", InvalidExpressionException, ERROR_INVALID_STRUCTURE),
        ("", InvalidExpressionException, ERROR_EMPTY_EXPRESSION),
    ]
)
def test_invalid_expressions(expression, expected_exception, error_message):
    with pytest.raises(expected_exception) as exif:
        evaluate(expression)
    assert str(exif.value) == error_message



@pytest.mark.parametrize(
    "expression, expected_exception, error_message",
    [
        ("1x = 5; x + 1", InvalidExpressionException, ERROR_INVALID_VARIABLE.format("1x")),
        ("x = 5; y + 1", InvalidExpressionException, ERROR_UNDEFINED_VARIABLE.format("y")),
        ("x = 5; z = y + 1; z", InvalidExpressionException, ERROR_UNDEFINED_VARIABLE.format("y")),
        ("x = 5; 5 +", InvalidExpressionException, ERROR_INVALID_STRUCTURE),
        ("x = 10; y = 0; x / y", InvalidExpressionException, ERROR_DIVISION_BY_ZERO),
    ],
)
def test_invalid_expressions_with_variables(expression, expected_exception, error_message):
    with pytest.raises(expected_exception) as exif:
        evaluate(expression)
    assert str(exif.value) == error_message
