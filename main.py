import json
import random
import sys
from pathlib import Path
from typing import List, Dict

import new_vocabulary_list

class ExitMessage(BaseException):
    pass


class Vocabulary:
    FORWARD_DIRECTION = "forwards"
    BACKWARDS_DIRECTION = "backwards"

    def __init__(self, sources: List, translations: List, source_example: str, target_example: str):
        self.translations = translations
        self.sources = sources
        self.source_example = source_example
        self.target_example = target_example
        self.quote = 50
        self._tries = 0
        self.tries_right = 0
        self.tries_false = 0
        self.current_question_direction = self.FORWARD_DIRECTION

    @classmethod
    def from_json(cls, json_data: Dict):
        example_data = json_data["example"]
        return cls(json_data["word"], json_data["translation"], example_data["source"], example_data["target"])

    @property
    def tries(self):
        return self._tries

    @tries.setter
    def tries(self, value):
        self._tries = value
        self.quote = 100 / (self.tries + 1) * (self.tries_right + 1 / (self.tries_false + 2))

    def next_try(self, input_name: str):
        if self.current_question_direction == self.FORWARD_DIRECTION:
            correct = (input_name in self.translations)
        else:
            correct = (input_name in self.sources)

        if correct:
            self.tries_right += 1
        else:
            self.tries_false += 1

        self.tries = self.tries_right + self.tries_false
        return correct

    def set_random_direction(self):
        self.current_question_direction = random.choice([self.FORWARD_DIRECTION, self.BACKWARDS_DIRECTION])

    @property
    def name(self) -> str:
        if self.current_question_direction == self.FORWARD_DIRECTION:
            return random.choice(self.sources)
        else:
            return random.choice(self.translations)

    def __repr__(self):
        return (f"{self.__class__.__name__}: "
                f"Name: {self.sources}, "
                f"To name: {self.translations}, "
                f"Quote {int(self.quote)}, "
                f"Tries right {self.tries_right}, "
                f"Tries false {self.tries_false}"
                f"Question Direction: {self.current_question_direction}"
                )


class Vocabularies:
    def __init__(self, vocabularies: List[Vocabulary], random_direction):
        self.vocabularies = vocabularies
        self.current_index = 0
        self.random_direction = random_direction

    @classmethod
    def from_json(cls, json_data, random_direction):
        vocabularies = [Vocabulary.from_json(vd) for vd in json_data]
        return cls(vocabularies, random_direction)

    def __add__(self, other: Vocabulary):
        if isinstance(other, Vocabulary):
            self.vocabularies.append(other)

    def get_new_vocabulary(self):
        probabilities = [1 / vocab.quote for vocab in self.vocabularies]
        self.current_index = random.choices(range(len(self.vocabularies)), weights=probabilities)[0]
        if self.random_direction:
            self.vocabularies[self.current_index].set_random_direction()
        return self.vocabularies[self.current_index]

    def next_try(self, name: str):
        return self.vocabularies[self.current_index].next_try(name)

    def get_state(self) -> tuple[int, int, int]:
        total_tries_right = sum([voc.tries_right for voc in self.vocabularies])
        total_tries = sum([voc.tries for voc in self.vocabularies])
        try:
            return (
                total_tries_right,
                total_tries,
                int(total_tries_right / total_tries * 100)  # Percent
            )
        except ZeroDivisionError:
            return 0, 0, 0


def get_path():
    # filedialog.askopenfilename(
    #         filetypes=[("JSON File", "*.json"), ("VOCABULARY File", "*.vocabularies")])
    raw_path = input_with_exit("Path (absolut): ")
    if not raw_path:
        print("No file selected")
        sys.exit()
    # print(f"Path is {Path(raw_path).absolute()}")
    return Path(raw_path)


def input_with_exit(prompt=""):
    text = input(prompt)
    if text == "%exit%":
        raise ExitMessage
    return text


def ask_vocabularies(vocabulary_path):
    vocabulary_list = []
    with open(vocabulary_path, encoding="utf-8") as file:
        for json_data in json.load(file)["entries"]:
            vocabulary_list.append(Vocabulary.from_json(json_data))

    vocabularies = Vocabularies(vocabulary_list, False)
    while True:
        vocabulary = vocabularies.get_new_vocabulary()
        name = input_with_exit(f"Other name of {vocabulary.name}: ")
        if name in ["exit", "stats"]:
            states = vocabularies.get_state()
            print(f"Your states:\n\tTotal: {states[0]}/{states[1]} ({states[2]}%)")
            if name == "exit":
                break
        elif name == "skip":
            print(f"It would be {vocabulary.translations}")
            continue
        else:
            is_right = vocabularies.next_try(name)
            print("Right" if is_right else "False",
                  f"{vocabulary.tries_right}/{vocabulary.tries}",
                  f"It would be {vocabulary.translations}" if not is_right else ""
                  )


def new_vocabulary_list():
    path = get_path()

    if not path.exists():
        if input_with_exit("Do you want to create this file? (y=Yes, n=No) ").lower() == "y":
            with open(path, "w") as file:
                json.dump(dict(entries=[""]), file)

    while True:
        names = []
        while True:
            if name := input_with_exit("Source name: "):
                names.append(name)
            else:
                break

        translations = []
        while True:
            if name := input_with_exit("Translation: "):
                translations.append(name)
            else:
                break

        source_example = input_with_exit("Source example: ")
        target_example = input_with_exit("Translation example: ")

        with open(path, "r+") as file:
            current_data = json.load(file)
            current_data["entries"].append({
                "word": names,
                "translation": translations,
                "example": {
                    "source": source_example,
                    "target": target_example
                }
            })
            file.seek(0)
            json.dump(current_data, file, indent=2)


TUTORIAL_TEXT = """
When you start this application, you will be asked what you want to do.
You must make a selection from the following to continue. 

o = open vocabulary file
n = new vocabulary file
t = Show this tutorial
c = Cancel

If you need to enter information, you can enter %exit% to exit

Important information:
Your statistics will not be saved!
"""

EXIT_MESSAGE = "Thanks for using"


def main():
    try:
        while True:
            print("""
            c = cancel,
            n = new vocabulary list
            o = open vocabulary list
            t = tutorial
            """)
            activity = input_with_exit("What want you to do? ").lower()
            if activity == "c":
                raise ExitMessage
            elif activity == "n":
                new_vocabulary_list()
            elif activity == "o":
                ask_vocabularies(get_path())
            elif activity == "t":
                print(TUTORIAL_TEXT)
    except ExitMessage:
        print(EXIT_MESSAGE)


if __name__ == '__main__':
    main()
