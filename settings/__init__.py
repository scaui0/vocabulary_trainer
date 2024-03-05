from pathlib import Path
from typing import Any

from settings.errors import CorrectionError, InvalidValueError
from settings.validators import StringValidator, IntegerValidator, BooleanValidator, FloatValidator


class Setting:
    """A base class for class Setting.

        Can be used to define various settings.

        Methods to be overridden:
            validate(value) -> bool
            correct(value) -> Any

        Attributes:
            value: The current value of the setting.
            display_name: The display name for the setting.
            name: The name (in lowercase) for the setting.
            description: The description of the setting.
        """

    def __init__(self, value: Any,
                 display_name: str,
                 name: str | None = None,
                 description: str = "",
                 correct_values: bool = False,
                 **kwargs):
        """Initializes a setting.

        Args:
            value: The initial value for the setting.
            display_name: The display name for the setting.
            name: The name (in lowercase) for the setting.
            description: The description of the setting.
            correct_values: Specified that it correct some values.
            kwargs: Please ignore this!
        """
        self._value = None
        self.value = value  # Sets value with validation
        self.display_name = display_name
        self.name = display_name.lower() if name is None else name
        self.description = description
        self.correct_values = correct_values

    def validate(self, value) -> bool:
        """Validates the value."""
        return True

    def correct(self, value) -> Any:
        """Corrects the value."""
        raise CorrectionError

    @classmethod
    def from_dict(cls, dct, name):
        return cls(dct[name], name)

    @property
    def value(self):
        """Get the value of the setting."""
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of the setting."""
        if self.validate(value):
            self._value = value
        elif not self.correct_values:
            raise InvalidValueError(value, self)
        else:
            try:
                corrected = self.correct(value)
            except CorrectionError:
                raise InvalidValueError(value, self)  # Can't be corrected
            if self.validate(corrected):  # Is corrected
                self._value = corrected
            else:  # Invalid again
                raise InvalidValueError(value, self)


class BooleanSetting(Setting, BooleanValidator):
    """Setting class for boolean values."""


class IntegerSetting(Setting, IntegerValidator):
    """Setting class for integer values."""


class FloatSetting(Setting, FloatValidator, ):
    """Setting class for float values."""


class StringSetting(Setting, StringValidator):
    """Setting class for string values."""


class DictionarySetting(Setting):
    def __init__(self, value: Any, display_name: str, name: str | None = None, description: str = "", **kwargs):
        super().__init__(value, display_name, name, description, **kwargs)

    def validate(self, value) -> bool:
        return isinstance(value, dict)

    def correct(self, value) -> Any:
        raise CorrectionError  # Can't be corrected

    def __getitem__(self, item):
        return self.value[item]

    def __setitem__(self, key, value):
        self.value[key] = value

    def __getattr__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError:
            try:
                return self[item]
            except KeyError:
                raise AttributeError(f"{self.__class__.__name__} has no attribute or setting {item!r}")

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            try:
                self[key] = value
            except KeyError:
                raise AttributeError(f"{self.__class__.__name__} has no attribute or setting {key!r}")


class Settings(dict):
    """A collection of settings."""
    def __init__(self, *settings: Setting):
        """Initializes the Settings object."""
        super().__init__({setting.name: setting for setting in settings})

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute or setting {item!r}")

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            try:
                self[key] = value
            except KeyError:
                raise AttributeError(f"{self.__class__.__name__} has no attribute or setting {key!r}")


def main():
    print(Settings.from_file(Path("settings.json")))


if __name__ == '__main__':
    main()
