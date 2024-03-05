from typing import Any

from settings import Setting, CorrectionError, Settings, IntegerSetting


class MySetting(Setting):
    def validate(self, value) -> bool:
        return value.islower() if isinstance(value, str) else False

    def correct(self, value) -> Any:
        if isinstance(value, str):
            return value.lower()
        else:
            raise CorrectionError


def main():
    setting = MySetting("foo", "Foo", "foo", "The foo")
    print(setting.value)

    setting.value = "bar"
    print(setting.value)

    setting.value = "FOO"  # Invalid, will raise InvalidValueException
    print(setting.value)

    setting = MySetting("foo", "Foo", "foo", "Bar")
    #  This Setting can't correct values
    setting.value = "HELLO WORLD"  # Invalid, will raise InvalidValueException

    #  ----------------------------

    settings = Settings(
        MySetting("bar", "Bar", "bar", "Desc.")
    )  # It will use the name attribut for indications

    print(settings)
    print(settings["bar"])  # Search by name attribut

    setting = IntegerSetting(1, "Int", "int", "Foo")
    setting.value = 5
    print(setting.value)
    setting.value = "6"  # Invalid, will raise InvalidValueException
    print(setting.value)




if __name__ == '__main__':
    main()
