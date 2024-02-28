from collections.abc import Iterable
from typing import Any


class CorrectionError(BaseException):
    """Raised when value correction fails."""


class Setting:
    """A base class for settings.

    Can be used to define various settings.

    Methods for override:
        validate(value) -> bool
        correct(value) -> Any

    Attributes:
        value: The current value of the setting.
        display_name: The display name for the setting.
        name: The name (in lowercase) for the setting.
        description: The description of the setting.
    """

    def __init__(self, value: Any, display_name: str, name: str | None = None, description: str = "", **kwargs):
        """Initializes a setting.


        :param value: The initial value for the setting.
        :param display_name: The display name for the setting.
        :param name: The name (in lowercase) for the setting.
        :param description: The description of the setting.
        :param **kwargs: Useless
        """
        self._value = None
        self.value = value  # Sets value with validation
        self.display_name = display_name
        self.name = display_name if name is None else name
        self.description = description

    def validate(self, value) -> bool:
        """Validates the value."""
        return True

    def correct(self, value) -> Any:
        """Corrects the value."""
        raise CorrectionError

    @property
    def value(self):
        """Get the value of the setting."""
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of the setting."""
        if self.validate(value):
            self._value = value
        else:
            try:
                corrected = self.correct(value)
            except CorrectionError:
                corrected = value

            if self.validate(corrected):
                self._value = corrected
            else:  # Invalid again
                raise ValueError(f"{value!r} is an invalid value for {self.__class__.__name__}")


class BooleanSetting(Setting):
    """Setting class for boolean values."""

    def validate(self, value) -> bool:
        """Validates the value."""
        return isinstance(value, bool)

    def correct(self, value) -> Any:
        """Corrects the value."""
        try:
            return bool(value)
        except ValueError:
            raise CorrectionError


class IntegerSetting(Setting):
    """Setting class for integer values."""

    def validate(self, value) -> bool:
        """Validates the value."""
        return isinstance(value, int)

    def correct(self, value) -> Any:
        """Corrects the value."""
        try:
            return int(value)
        except ValueError:
            raise CorrectionError


class FloatSetting(Setting):
    """Setting class for float values."""

    def validate(self, value) -> bool:
        """Validates the value."""
        return isinstance(value, float)

    def correct(self, value) -> Any:
        """Corrects the value."""
        try:
            return float(value)
        except ValueError:
            raise CorrectionError


class StringSetting(Setting):
    """Setting class for string values."""

    def validate(self, value) -> bool:
        """Validates the value."""
        return isinstance(value, str)

    def correct(self, value) -> Any:
        """Corrects the value."""
        return str(value)


class Settings(Iterable):
    """A collection of settings."""

    def __init__(self, *settings: Setting):
        """Initializes the Settings object."""
        self.settings = {setting.display_name: setting for setting in settings}

    def __iter__(self):
        """Iterates over settings."""
        yield from self.settings.values()

    def __getitem__(self, item):
        """Gets a setting by display name."""
        return self.settings[item]

    def __setitem__(self, key, value: Setting):
        """Sets a setting."""
        if isinstance(value, Setting):
            self.settings[key] = value

    def add_setting(self, setting: Setting, name: str | None = None):
        """Adds a new setting."""
        setting_name = setting.name if name is None else name
        self.settings[setting_name] = setting

    def __repr__(self):
        return self.settings.__repr__()


def main():
    # Create a settings collection
    settings = Settings(StringSetting("Franz", "name"), IntegerSetting(13, "age"))
    settings.add_setting(BooleanSetting(False, "has_siblings"))

    # Modify a setting value
    settings["has_siblings"].value = True

    # Print settings
    print(settings, BooleanSetting(value="Hallo", display_name=""))


if __name__ == '__main__':
    main()
