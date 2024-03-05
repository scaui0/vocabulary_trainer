from typing import Any

from settings.errors import CorrectionError


class BooleanValidator:
    def validate(self, value) -> bool:
        return isinstance(value, str)

    def correct(self, value) -> Any:
        return str(value)


class StringValidator:
    def validate(self, value) -> bool:
        return isinstance(value, str)

    def correct(self, value) -> Any:
        return str(value)


class IntegerValidator:
    def validate(self, value) -> bool:
        return isinstance(value, int)

    def correct(self, value) -> Any:
        try:
            return int(value)
        except ValueError:
            raise CorrectionError


class FloatValidator:
    def validate(self, value) -> bool:
        """Validates the value."""
        return isinstance(value, float)

    def correct(self, value) -> Any:
        """Corrects the value."""
        try:
            return float(value)
        except ValueError:
            raise CorrectionError
