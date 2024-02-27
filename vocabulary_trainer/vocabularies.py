import dataclasses
import json
import random
from typing import List, Tuple

with open("Vocabulary Schema.json", encoding="utf-8") as file:
    JSONSCHEMA = json.load(file)


@dataclasses.dataclass
class Stats:
    tries_right: int
    tries_false: int
    _tries_total: int = dataclasses.field(init=False, default=0)
    quote: int = dataclasses.field(init=False, default=0)

    def __post_init__(self):
        self._update_total_tries()

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data["tries_right"], json_data["tries_total"])

    def right_try(self, points=1):
        self.tries_right += points
        self._update_total_tries()

    def false_try(self, points=1):
        self.tries_false += points
        self._update_total_tries()

    @property
    def tries_total(self):
        return self._tries_total

    def _update_total_tries(self):
        self._tries_total = self.tries_right + self.tries_false
        self.quote = int(((self.tries_right + 1) / (self._tries_total + 1)) * 100)


class SimpleVocabulary:
    def __init__(self, sources: List[str], translations: List[str], source_example: str, target_example: str,
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

    def next_try(self, name):
        if name in self.translations:
            self.stats.right_try()
            return (True,)
        else:
            self.stats.false_try()
            return False, self.translations

    def __repr__(self):
        return f"{self.sources}: {self.translations}"


class Vocabulary:
    FORWARD_DIRECTION = "forwards"
    BACKWARD_DIRECTION = "backwards"

    def __init__(self, sources: List[str], translations: List[str], source_example: str, target_example: str,
                 stats: Stats, random_direction=True):

        self.forward_vocabulary = SimpleVocabulary(sources, translations, source_example, target_example, stats)
        self.backward_vocabulary = SimpleVocabulary(translations, sources, target_example, source_example, stats)

        self.direction = self.FORWARD_DIRECTION
        self.random_direction = random_direction
        self.states = stats

    @classmethod
    def from_json(cls, json_data, random_direction=True):
        example = json_data["examples"]
        return cls(json_data["sources"], json_data["targets"], example["source"], example["target"],
                   Stats.from_json(json_data["stats"]), random_direction)

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

    def next_try(self, name) -> Tuple[bool, List[str] | None]:
        if self.direction == self.FORWARD_DIRECTION:
            response = self.forward_vocabulary.next_try(name)
        else:
            response = self.backward_vocabulary.next_try(name)

        return response

    def set_random_direction(self):
        if self.random_direction:
            self.direction = random.choice([self.FORWARD_DIRECTION, self.BACKWARD_DIRECTION])

    def __repr__(self):
        return self.forward_vocabulary.__repr__()


class VocabularyWithSubvocabularies:
    def __init__(self, main_vocabulary, vocabularies):
        self.main_vocabulary = main_vocabulary
        self.vocabularies = vocabularies
        self.all_vocabularies: List[Vocabulary] = vocabularies + [self.main_vocabulary]
        self.current_index = 0

    @classmethod
    def from_json(cls, json_data):
        vocabularies = [Vocabulary.from_json(data) for data in json_data["subentries"]]
        return cls(Vocabulary.from_json(json_data), vocabularies)

    def get_new_vocabulary(self):
        self.current_index = random.randint(0, len(self.all_vocabularies) - 1)
        self.all_vocabularies[self.current_index].set_random_direction()
        return self.all_vocabularies[self.current_index].source

    def next_try(self, name):
        return self.all_vocabularies[self.current_index].next_try(name)

    @property
    def translation(self):
        return self.all_vocabularies[self.current_index].translation

    @property
    def source(self):
        return self.all_vocabularies[self.current_index].source

    @property
    def translations(self):
        return self.all_vocabularies[self.current_index].translations

    @property
    def sources(self):
        return self.all_vocabularies[self.current_index].sources

    def __repr__(self):
        return self.all_vocabularies.__repr__()


class VocabularyList:
    def __init__(self, vocabularies: List[VocabularyWithSubvocabularies]):
        self.vocabularies = vocabularies
        self.current_index = 0

    @classmethod
    def from_json(cls, json_data):
        vocabularies = [VocabularyWithSubvocabularies.from_json(voc_data) for voc_data in json_data["entries"]]
        return cls(vocabularies)

    def get_new_vocabulary(self):
        self.current_index = random.randint(0, len(self.vocabularies) - 1)
        return self.vocabularies[self.current_index].get_new_vocabulary()

    def next_try(self, name):
        return self.vocabularies[self.current_index].next_try(name)

    def __repr__(self):
        return self.vocabularies.__repr__()
