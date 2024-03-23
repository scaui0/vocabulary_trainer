import dataclasses
import json
import operator
import random
from pathlib import Path
from typing import List, Tuple

JSONSCHEMA = json.loads((Path(__file__).parent / "Vocabulary Schema.json").read_text("utf-8"))


def better_sum(iterable):
    result = iterable[0]
    for item in iterable[1:]:
        result = result + item
    return result


@dataclasses.dataclass
class Stats:
    right_tries: int
    wrong_tries: int
    _total_tries: int = dataclasses.field(init=False, default=0)
    quote: int = dataclasses.field(init=False, default=0)

    def __post_init__(self):
        self._update_total_tries()

    @classmethod
    def from_dict(cls, json_data):
        return cls(json_data["tries_right"], json_data["tries_total"])

    def to_json(self) -> dict:
        return dict(
            tries_total=self.tries_total,
            tries_right=self.right_tries,
            tries_wrong=self.wrong_tries
        )

    def right_try(self, points=1):
        self.right_tries += points
        self._update_total_tries()

    def wrong_try(self, points=1):
        self.wrong_tries += points
        self._update_total_tries()

    @property
    def tries_total(self):
        return self._total_tries

    def _update_total_tries(self):
        self._total_tries = self.right_tries + self.wrong_tries
        self.quote = int(((self.right_tries + 1) / (self._total_tries + 1)) * 100)

    def _compare(self, other, func):
        if isinstance(other, Stats):
            return func(self.quote, other.quote)
        else:
            return NotImplemented

    def __le__(self, other):
        return self._compare(other, operator.le)

    def __lt__(self, other):
        return self._compare(other, operator.lt)

    def __eq__(self, other):
        return self._compare(other, operator.eq)

    def __ne__(self, other):
        return self._compare(other, operator.ne)

    def __ge__(self, other):
        return self._compare(other, operator.ge)

    def __gt__(self, other):
        return self._compare(other, operator.gt)

    @staticmethod
    def _math_helper(self, other, func):
        if isinstance(other, Stats):
            return Stats(
                func(self.right_tries, other.right_tries),
                func(self.wrong_tries, other.wrong_tries)
            )
        else:
            return NotImplemented

    def __add__(self, other):
        return self._math_helper(self, other, operator.add)


class _SimpleVocabulary:
    def __init__(self, sources: Tuple[str], translations: Tuple[str], source_example: str, target_example: str,
                 stats: Stats):
        self.stats = stats
        self.target_example = target_example
        self.source_example = source_example
        self.translations = translations
        self.sources = sources

    @property
    def translation(self):
        return random.choice(self.translations)

    @property
    def source(self):
        return random.choice(self.sources)

    def next_try(self, name) -> Tuple[bool, Tuple[str] | None]:
        if name in self.translations:
            self.stats.right_try()
            return True, None
        else:
            self.stats.wrong_try()
            return False, tuple(self.translations)

    def __repr__(self):
        return f"{self.sources}: {self.translations}"


class Vocabulary:
    FORWARD_DIRECTION = "forwards"
    BACKWARD_DIRECTION = "backwards"

    def __init__(self, sources: Tuple[str], translations: Tuple[str], source_example: str, target_example: str,
                 stats: Stats, random_direction=True):

        self.forward_vocabulary = _SimpleVocabulary(sources, translations, source_example, target_example, stats)
        self.backward_vocabulary = _SimpleVocabulary(translations, sources, target_example, source_example, stats)

        self.direction = self.FORWARD_DIRECTION
        self.random_direction = random_direction
        self.states = stats

    @classmethod
    def from_json(cls, json_data, random_direction=True):
        example = json_data["examples"]
        return cls(json_data["sources"], json_data["targets"], example["source"], example["target"],
                   Stats.from_dict(json_data["stats"]), random_direction)

    def to_json(self) -> dict:
        return dict(
            sources=self.sources,
            targets=self.translations,
            stats=self.states.to_json(),
            examples=dict(
                target=self.target_example,
                source=self.source_example
            )
        )

    @property
    def translation(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.translation
        else:
            return self.backward_vocabulary.translation

    @property
    def translations(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.translations
        else:
            return self.backward_vocabulary.translations

    @property
    def source(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.source
        else:
            return self.backward_vocabulary.source

    @property
    def sources(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.sources
        else:
            return self.backward_vocabulary.sources

    @property
    def target_example(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.target_example
        else:
            return self.backward_vocabulary.target_example

    @property
    def source_example(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.source_example
        else:
            return self.backward_vocabulary.source_example

    def next_try(self, name) -> Tuple[bool, Tuple[str] | None]:
        if self.direction == self.FORWARD_DIRECTION:
            response = self.forward_vocabulary.next_try(name)
        else:
            response = self.backward_vocabulary.next_try(name)

        return response

    def randomize_vocabulary_direction(self):
        if self.random_direction:
            self.direction = random.choice([self.FORWARD_DIRECTION, self.BACKWARD_DIRECTION])

    def __repr__(self):
        return self.forward_vocabulary.__repr__()


class TreeVocabulary:
    def __init__(self, main_vocabulary: Vocabulary, vocabularies):
        self._main_vocabulary = main_vocabulary
        self._vocabularies = vocabularies
        self.all_vocabularies: List[Vocabulary] = vocabularies + [self._main_vocabulary]
        self.current_vocabulary = None

    @classmethod
    def from_dict(cls, json_data):
        vocabularies = [Vocabulary.from_json(data) for data in json_data["subentries"]]
        return cls(Vocabulary.from_json(json_data), vocabularies)

    def to_json(self):
        return dict(**self._main_vocabulary.to_json(),
                    subentries=[voc.to_json() for voc in self._vocabularies])

    def get_new_vocabulary(self):
        self.current_vocabulary = random.choices(
            self.all_vocabularies,
            weights=[voc.states.quote / 100 for voc in self.all_vocabularies]
        )[0]

        self.current_vocabulary.randomize_vocabulary_direction()
        return self.current_vocabulary.source

    def next_try(self, name):
        return self.current_vocabulary.next_try(name)

    @property
    def translation(self):
        return self.current_vocabulary.translation

    @property
    def source(self):
        return self.current_vocabulary.source

    @property
    def translations(self):
        return self.current_vocabulary.translations

    @property
    def sources(self):
        return self.current_vocabulary.sources

    @property
    def target_example(self):
        return self.current_vocabulary.target_example

    @property
    def source_example(self):
        return self.current_vocabulary.source_example

    @property
    def states(self):
        x = better_sum([voc.states for voc in self.all_vocabularies])
        return x

    def __repr__(self):
        return self.all_vocabularies.__repr__()


class VocabularyList:
    def __init__(self, vocabularies: List[TreeVocabulary]):
        self.vocabularies = vocabularies
        self.current_vocabulary = None

    @classmethod
    def from_dict(cls, json_data):
        vocabularies = [TreeVocabulary.from_dict(voc_data) for voc_data in json_data["entries"]]
        return cls(vocabularies)

    def to_json(self):
        return self.vocabularies

    def get_new_vocabulary(self) -> str:
        self.current_vocabulary = random.choices(
            self.vocabularies,
            weights=[voc.states.quote / 100 for voc in self.vocabularies]
        )[0]
        return self.current_vocabulary.get_new_vocabulary()

    def next_try(self, name):
        return self.current_vocabulary.next_try(name)

    def skip(self):
        return self.current_vocabulary.translations

    def __iter__(self):
        """Iterate over vocabularies (sorted)"""
        yield from self.vocabularies

    def __repr__(self):
        return self.vocabularies.__repr__()


class Vocabularies(VocabularyList):
    def __init__(self, vocabularies: List[TreeVocabulary], name, has_random_direction=True):
        super().__init__(vocabularies)

        self.name = name
        self.random_direction = has_random_direction

    @classmethod
    def from_dict(cls, json_data):
        vocabularies = [TreeVocabulary.from_dict(voc_data) for voc_data in json_data["entries"]]
        return cls(vocabularies, json_data["name"], json_data["random_direction"])

    @classmethod
    def from_file(cls, path, encoding="utf-8"):
        with open(path, "r", encoding=encoding) as file:
            return cls.from_dict(json.load(file))

    def to_json(self):
        return dict(
            entries=[voc.to_json() for voc in self.vocabularies],
            name=self.name,
            random_direction=self.random_direction
        )


def main():
    a = Vocabularies.from_file("testvokabeln.json")
    print(json.dumps(a.to_json(), indent=2))


if __name__ == '__main__':
    main()
