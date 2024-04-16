import json
from os import PathLike
from pathlib import Path
from typing import List, Dict, LiteralString


class LanguageNotSupportedError(BaseException):
    pass


class LanguageFileNotFoundError(BaseException):
    pass


All_LANGUAGES = "all"


class Translator:
    def __init__[All_LANGUAGES: LiteralString["all"]] \
                    (self, main_dir: PathLike | str,
                     default_language="en",
                     supported_languages: All_LANGUAGES | List[str] = All_LANGUAGES):

        self.current_language = default_language
        self.supported_languages = supported_languages
        self.translation_dir = main_dir
        self._translations = {}

        self.install(default_language)

    def install(self, language):
        if self.supported_languages != All_LANGUAGES and language not in self.supported_languages:
            raise LanguageNotSupportedError(f"Language {language!r} is not supported!")

        language_path = Path(self.translation_dir, f"{language}.json")

        if not language_path.exists():
            raise LanguageFileNotFoundError(
                f"Translation file {language!r}.json not found in folder '{self.translation_dir}'"
            )

        with language_path.open("r", encoding="utf-8") as file:
            self._translations[language] = json.load(file)
        self.current_language = language

    def translate(self, key):
        try:
            return self._translations[self.current_language][key]
        except KeyError:
            return key
