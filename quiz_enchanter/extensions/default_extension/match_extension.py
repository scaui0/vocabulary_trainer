import re

from quiz_enchanter import Plugin, BaseModel


plugin = Plugin.get_plugin("default")
match_quiz_type = plugin.quiz_type("match", "Match")


@match_quiz_type.model
class MatchModel(BaseModel):
    def __init__(self, json_data):
        self.question = json_data["question"]
        self.strip_start_and_end = json_data.get("strip_start_and_end", True)
        self.ignore_case = json_data.get("ignore_case", False)
        self.regex = json_data.get("regex", None)

        right = json_data["right"]
        self.right = right if isinstance(right, list) else [right]  # Multiple right answers are allowed!

        self.selection = None

    @property
    def is_right(self):
        base_selection = self.selection.strip() if self.strip_start_and_end else self.selection
        selection = base_selection.lower() if self.ignore_case else base_selection

        if self.regex is None:
            return selection in self.right
        else:
            return bool(re.match(self.regex, selection))


@match_quiz_type.cli
def run(model):
    print(model.question)
    model.selection = input("Answer: ")

    return model.is_right
