from collections.abc import Iterable
from typing import Any


class CorrectionError(BaseException):
    pass


class Setting:
    def __init__(self, value: Any, display_name: str, name: str | None = None, description: str = ""):
        """
        :parameter value The init value.
        :parameter display_name The display name for the setting
        :parameter name The name (in lowercase)
        :parameter description The description
    """
        self._value = None
        self.value = value  # Sets value with validation
        self.display_name = display_name
        self.name = display_name if name is None else name
        self.description = description

    def validate(self, value) -> bool:
        """Validates the value"""
        return True

    def correct(self, value) -> Any:
        """Correct the value"""
        raise CorrectionError

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
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

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name!r}: {self.value}>"


class BooleanSetting(Setting):
    """Setting class for bools (Booleans)"""
    def validate(self, value) -> bool:
        return isinstance(value, bool)

    def correct(self, value) -> Any:
        try:
            return bool(value)
        except ValueError:
            raise CorrectionError


class IntegerSetting(Setting):
    """Setting class for ints (Integers)"""
    def validate(self, value) -> bool:
        return isinstance(value, int)

    def correct(self, value) -> Any:
        try:
            return int(value)
        except ValueError:
            raise CorrectionError


class FloatSetting(Setting):
    """Setting class for floats"""
    def validate(self, value) -> bool:
        return isinstance(value, float)

    def correct(self, value) -> Any:
        try:
            return float(value)
        except ValueError:
            raise CorrectionError


class StringSetting(Setting):
    """Setting class for some strings"""
    def validate(self, value) -> bool:
        return isinstance(value, str)

    def correct(self, value) -> Any:
        return str(value)


class Settings(Iterable):
    def __init__(self, *settings: Setting):
        self.settings = {setting.display_name: setting for setting in settings}

    def __iter__(self):
        yield from self.settings.values()

    def __getitem__(self, item):
        return self.settings[item]

    def __setitem__(self, key, value: Setting):
        if isinstance(value, Setting):
            self.settings[key] = value

    def add_setting(self, setting: Setting, name: str | None = None):
        setting_name = setting.name if name is None else name
        self.settings[setting_name] = setting

    def __repr__(self):
        return self.settings.__repr__()


def main():
    settings = Settings(StringSetting("Franz", "name"), IntegerSetting(13, "age"))
    settings.add_setting(BooleanSetting(False, "has_siblings"))
    settings["has_siblings"].value = True
    print(settings, BooleanSetting(value="Hallo", display_name=""))


if __name__ == '__main__':
    main()
