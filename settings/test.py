import json
from pathlib import Path

import yaml

from settings import Settings, StringSetting, IntegerSetting, BooleanSetting, DictionarySetting


class TestMeta(type):
    def __new__(cls, name, bases, dct):
        build_class = super().__new__(cls, name, bases, dct)

        build_class.__fields__ = build_class.__annotations__
        for annot, call in build_class.__fields__.items():
            if not callable(call):
                if callable(call.__class__):
                    build_class.__fields__[annot] = call.__class__

        return build_class


class SettingTemplate(metaclass=TestMeta):
    @classmethod
    def load_from_file(cls, path: Path | str, **kwargs):
        path = Path(path)
        with path.open(encoding="utf-8") as file:
            if path.suffix == ".json":
                dct: dict = json.load(file)
            elif path.suffix == ".yml":
                dct: dict = yaml.safe_load(file)
            else:
                raise FileNotFoundError("Invalid file format")

        settings = []
        for key, value in dct.items():
            settings.append(cls.__fields__[key](value, key, **kwargs))

        return Settings(*settings)


class Template(SettingTemplate):
    name: StringSetting
    age: IntegerSetting


def main():
    a = Template.load_from_file("settings.json")
    print(a.items())


if __name__ == "__main__":
    main()
