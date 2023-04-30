from lib.validators import Validator
import pytest


def test_validator():
    validator = Validator("John")

    # Add a valid checker that should not raise an exception
    validator.add(lambda x: len(x) > 0, "Invalid input")

    # Add an invalid checker that should raise a ValueError
    validator.add(lambda x: len(x) < 2, "Input length should be at least 2")

    # Check that the validation works correctly
    with pytest.raises(ValueError):
        validator.check()

    # Add another invalid checker that should raise a different ValueError
    validator.add(lambda x: len(x) > 5, "Input length should be at most 5")

    # Check that the validation works correctly with multiple checkers
    with pytest.raises(ValueError):
        validator.check()
