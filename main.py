import json
import random
import sys
from pathlib import Path
from typing import List, Dict

from translator import MultipleLanguageTranslator

translator = MultipleLanguageTranslator(Path("translations"))
translator.install("de")
_ = translator.translate


class ExitMessage(BaseException):
    pass


class GoToMainMenuMessage(BaseException):
    pass


class Vocabulary:
    FORWARD_DIRECTION = "forwards"
    BACKWARDS_DIRECTION = "backwards"

    def __init__(self, sources: List, translations: List, source_example: str, target_example: str):
        self._translations = translations
        self.sources = sources
        self.source_example = source_example
        self.target_example = target_example
        self.quote = 50
        self.tries = 0
        self.tries_right = 0
        self.tries_false = 0
        self.current_question_direction = self.FORWARD_DIRECTION

    @classmethod
    def from_json(cls, json_data: Dict):
        example_data = json_data["example"]
        return cls(json_data["word"], json_data["translation"], example_data["source"], example_data["target"])

    def next_try(self, input_name: str):
        if self.current_question_direction == self.FORWARD_DIRECTION:
            correct = (input_name in self._translations)
        elif self.current_question_direction == self.BACKWARDS_DIRECTION:
            correct = (input_name in self.sources)
        else:
            raise OSError(f"self.direction is invalid. It is {self.current_question_direction}\n{self!r}")

        if correct:
            self.tries_right += 1
        else:
            self.tries_false += 1

        self.tries = self.tries_right + self.tries_false
        try:
            self.quote = 100 * ((self.tries + 1) / (self.tries_right + 1))
        except ZeroDivisionError:
            self.quote = 0
        return correct

    def set_random_direction(self):
        self.current_question_direction = random.choice([self.FORWARD_DIRECTION, self.BACKWARDS_DIRECTION])

    @property
    def name(self) -> str:
        if self.current_question_direction == self.FORWARD_DIRECTION:
            return random.choice(self.sources)
        elif self.current_question_direction == self.BACKWARDS_DIRECTION:
            return random.choice(self._translations)
        else:
            print(_("trainer.vocabulary.error.directions"))

    @property
    def translation(self) -> str:
        if self.current_question_direction == self.FORWARD_DIRECTION:
            return random.choice(self._translations)
        elif self.current_question_direction == self.BACKWARDS_DIRECTION:
            return random.choice(self.sources)
        else:
            raise OSError(f"self.direction is invalid. It is {self.current_question_direction}\n{self!r}")

    @property
    def translations(self):
        if self.current_question_direction == self.FORWARD_DIRECTION:
            return self._translations
        elif self.current_question_direction == self.BACKWARDS_DIRECTION:
            return self.sources
        else:
            raise OSError(f"self.direction is invalid. It is {self.current_question_direction}\n{self!r}")

    def __str__(self):
        return (f"{self.__class__.__name__}: "
                f"Name: {self.sources}, "
                f"To name: {self._translations}, "
                f"Quote {int(self.quote)}, "
                f"Tries right {self.tries_right}, "
                f"Tries false {self.tries_false}"
                f"Question Direction: {self.current_question_direction}"
                )


class Vocabularies:
    def __init__(self, vocabularies: List[Vocabulary], random_direction=False):
        self.vocabularies = vocabularies
        self.current_index = 0
        self.random_direction = random_direction

    @classmethod
    def from_json(cls, json_data, random_direction):
        vocabularies = [Vocabulary.from_json(vd) for vd in json_data]
        return cls(vocabularies, random_direction)

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
    raw_path = input_with_exit(_("trainer.path.get_path"))
    if not raw_path:
        print(_("trainer.path.no_selected"))
        sys.exit()
    # print(f"Path is {Path(raw_path).absolute()}")
    return Path(raw_path)


def input_with_exit(prompt=""):
    text = input(prompt)
    if text == "%exit%":
        raise ExitMessage
    elif text == "%main%":
        raise GoToMainMenuMessage
    return text


def ask_vocabularies(vocabulary_path):
    vocabulary_list = []
    with open(vocabulary_path, encoding="utf-8") as file:
        for json_data in json.load(file)["entries"]:
            vocabulary_list.append(Vocabulary.from_json(json_data))

    vocabularies = Vocabularies(vocabulary_list, True)
    while True:
        vocabulary = vocabularies.get_new_vocabulary()
        name = input_with_exit(_("trainer.ask.translated").format(repr(vocabulary.name)))
        if name == "stats":
            states = vocabularies.get_state()
            print(_("trainer.ask.states").format(*states))
        elif name == "skip":
            print(_("trainer.ask.it_would").format(
                vocabulary.name))
            continue
        elif name == "bug":
            print(vocabularies.vocabularies)
        else:
            is_right = vocabularies.next_try(name)
            print(_("trainer.ask.right") if is_right else _("trainer.ask.false"),
                  _("trainer.ask.tries").format(vocabulary.tries_right, vocabulary.tries),
                  _("trainer.ask.it_would").format(vocabulary.translations) if not is_right else ""
                  )


def new_vocabulary_list():
    path = get_path()

    if not path.exists():
        if input_with_exit(_("trainer.new_file.create_file")).lower() == "y":
            with open(path, "w") as file:
                json.dump(dict(entries=[""]), file)

    while True:
        names = []
        while True:
            if name := input_with_exit(_("trainer.new_file.source")):
                names.append(name)
            else:
                break

        translations = []
        while True:
            if name := input_with_exit(_("trainer.new_file.translation")):
                translations.append(name)
            else:
                break

        source_example = input_with_exit(_("trainer.new_file.source.example"))
        target_example = input_with_exit(_("trainer.new_file.translation.example"))

        with open(path, "r+") as file:
            current_data = json.load(file)
            current_data["entries"].append(
                dict(
                    word=names,
                    translation=translations,
                    example=dict(source=source_example, target=target_example)
                )
            )
            file.seek(0)
            json.dump(current_data, file, indent=2)


MAIN_PROMPT = _("trainer.main.prompt_help")

TUTORIAL_TEXT = _("trainer.tutorial").format(MAIN_PROMPT)

WELCOME_MESSAGE = _("trainer.welcome")

ACTION_QUESTION = _("trainer.main.ask_action")

INVALID_ACTION = _("trainer.main.ask_action.invalid")

EXIT_MESSAGE = _("trainer.thanks_for_using")


def main():
    print(WELCOME_MESSAGE)
    while True:
        try:
            print(MAIN_PROMPT)
            activity = input_with_exit(ACTION_QUESTION)
            activity_low = activity.lower()
            if activity_low == "c":
                raise ExitMessage
            elif activity_low == "n":
                new_vocabulary_list()
            elif activity_low == "o":
                ask_vocabularies(get_path())
            elif activity_low == "t":
                print(TUTORIAL_TEXT)
            else:
                print(INVALID_ACTION.format(action=repr(activity)))
        except GoToMainMenuMessage:
            continue
        except ExitMessage:
            print(EXIT_MESSAGE)
            return


if __name__ == '__main__':
    main()
