import json
from os import PathLike
from pathlib import Path
from typing import List, Dict


class OneLanguageTranslator:
    def __init__(self, path: PathLike, encoding="utf-8"):
        with open(path, encoding=encoding) as file:
            self.translations = json.load(file)

    def translate(self, path: str):
        if path in self.translations:
            return self.translations[path]
        else:
            return path

    tr = translate


All_LANGUAGES = "all"


class LanguageNotSupportedError(BaseException):
    pass


class BaseTranslator:
    def __init__(self, translations: Dict[str, Dict[str, str]],
                 default_language="en", supported_languages: str | List[str] = All_LANGUAGES):
        self._translations = translations
        self.current_language = default_language
        self.supported_languages = supported_languages

        self.install(default_language)

    def install(self, language):
        if language in self.supported_languages or self.supported_languages == All_LANGUAGES:
            self.current_language = language
        else:
            raise LanguageNotSupportedError(f"{self.__class__.__name__} doesn't support language {language!r}")

    def translate(self, key):
        try:
            return self._translations[self.current_language][key]
        except KeyError:
            return key


class MultipleLanguageTranslator(BaseTranslator):
    def __init__(self, main_dir: PathLike, default_language="en", supported_languages: List[str] | str = All_LANGUAGES):
        self.translation_dir = main_dir
        super().__init__({}, default_language, supported_languages)

    def install(self, language):
        super().install(language)

        try:
            with Path(self.translation_dir, f"{self.current_language}.json").open("r", encoding="utf-8") as file:
                self._translations[self.current_language] = json.load(file)
        except FileNotFoundError:
            text = f"Translation file {self.current_language!r}.json not found in folder '{self.translation_dir}'"
            raise FileNotFoundError(text) from None


def main():
    translator = MultipleLanguageTranslator(Path("translations"), "en", ["de", "en"])

    for lang in ["de", "en"]:
        translator.install(lang)
        print(translator.translate("message.error.test"))
        print(translator.translate("message.test.welcome"))


if __name__ == "__main__":
    main()
