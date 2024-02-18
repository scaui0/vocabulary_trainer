import dataclasses
import random
from typing import List


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


class Vocabulary:
    FORWARD_DIRECTION = "forwards"
    BACKWARD_DIRECTION = "backwards"

    def __init__(self, sources: List[str], translations: List[str], source_example: str, target_example: str,
                 stats: Stats, random_direction=True, tries=1):

        self.forward_vocabulary = SimpleVocabulary(sources, translations, source_example, target_example, stats)
        self.backward_vocabulary = SimpleVocabulary(translations, sources, target_example, source_example, stats)

        self.direction = self.FORWARD_DIRECTION
        self.random_direction = random_direction
        self.max_tries = tries
        self.current_tries = 0

    @classmethod
    def from_json(cls, json_data):
        example = json_data["example"]
        return cls(json_data["sources"], json_data["translations"], example["source"], example["target"],
                   Stats.from_json(json_data["stats"]))

    @property
    def translation(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.translation
        else:
            return self.backward_vocabulary.translation

    @property
    def source(self):
        if self.direction == self.FORWARD_DIRECTION:
            return self.forward_vocabulary.source
        else:
            return self.backward_vocabulary.source

    def next_try(self, name):
        self.max_tries += 1
        if self.direction == self.FORWARD_DIRECTION:
            response = self.forward_vocabulary.next_try(name)
        else:
            response = self.backward_vocabulary.next_try(name)

        return response


def main():
    pass
