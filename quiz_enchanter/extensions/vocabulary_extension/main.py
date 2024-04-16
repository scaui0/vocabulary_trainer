import json
import random
from pathlib import Path

from quiz_enchanter import Tries


class Vocabulary:
    FORWARDS_DIRECTION = "forwards"
    BACKWARDS_DIRECTION = "backwards"
    DIRECTIONS = FORWARDS_DIRECTION, BACKWARDS_DIRECTION

    def __init__(self, sources, translations, source_example, target_example, tries):
        self.tries = tries
        self.target_example = target_example
        self.source_example = source_example
        self.translations = translations
        self.sources = sources
        self.direction = self.FORWARDS_DIRECTION

    @classmethod
    def from_json(cls, json_data):
        return cls(
            sources=json_data["sources"],
            translations=json_data["translations"],
            source_example=json_data["source_example"],
            target_example=json_data["target_example"],
            tries=Tries.from_json(json_data["stats"])
        )

    def randomize(self):
        self.direction = random.choice(self.DIRECTIONS)

    @property
    def source(self):
        if self.direction == self.FORWARDS_DIRECTION:
            return random.choice(self.sources)
        else:
            return random.choice(self.translations)

    @property
    def translation(self):
        if self.direction == self.FORWARDS_DIRECTION:
            return random.choice(self.translations)
        else:
            return random.choice(self.sources)

    @property
    def json(self):
        return dict(
            sources=self.sources,
            translations=self.translations,
            source_example=self.source_example,
            target_example=self.target_example,
            stats=self.tries.json
        )

    def check(self, name):
        if self.direction == self.FORWARDS_DIRECTION:
            is_right = name in self.translations
        else:
            is_right = name in self.sources

        if is_right:
            return is_right,
        else:
            if self.direction == self.FORWARDS_DIRECTION:
                return is_right, self.translations
            else:
                return is_right, self.sources


    def __repr__(self):
        # Short: {self.sources[0]}
        return f"{self.__class__.__name__}(sources={self.sources}, translations={self.translations})"

    def __str__(self):
        return f"{self.sources[0]}-{self.translations[0]}"


class Vocabularies:
    def __init__(self, *vocabularies):
        self.vocabularies = vocabularies
        self.current_vocabulary = None

    @classmethod
    def from_json(cls, json_data):
        vocabularies = []
        for data in json_data["entries"]:
            match data:
                case {"entries": _}:
                    vocabularies.append(Vocabularies.from_json(data))
                case _:
                    vocabularies.append(Vocabulary.from_json(data))

        return cls(*vocabularies)

    @property
    def json(self):
        return dict(
            entries=[voc.json for voc in self.vocabularies]
        )

    def __iter__(self):
        while True:
            yield self.random_vocabulary

    def __repr__(self):
        return repr(self.vocabularies)

    @property
    def random_vocabulary(self):
        selected_vocabulary = random.choices(self.vocabularies,
                                             weights=[voc.tries.reciprocal for voc in self.vocabularies],
                                             k=1)[0]  # Select one Element
        if isinstance(selected_vocabulary, Vocabulary):
            self.current_vocabulary = selected_vocabulary  # Without sub vocabularies
        else:
            self.current_vocabulary = selected_vocabulary.random_vocabulary  # With sub vocabularies

        return self.current_vocabulary

    def check(self, name):
        return self.current_vocabulary.check(name)


if __name__ == '__main__':
    with open(Path(__file__).parent / "test_vocabularies.json", encoding="utf-8") as file:
        a = Vocabularies.from_json(json.load(file))
    while True:
        print(a.random_vocabulary.source)
        print(a.check(input("Voc: ")))
