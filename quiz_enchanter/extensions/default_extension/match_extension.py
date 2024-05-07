from quiz_enchanter import Plugin, BaseModel


plugin = Plugin.get_plugin("default")
match_quiz_type = plugin.quiz_type("match", "Match")


@match_quiz_type.model
class MatchModel(BaseModel):
    def __init__(self, json_data):
        self.question = json_data["question"]
        self.right = json_data["right"]
        self.strip_start_and_end = json_data.get("strip_start_and_end", True)

        self.selection = None

    @property
    def is_right(self):
        selection = self.selection.strip() if self.strip_start_and_end else self.selection
        return selection == self.right


@match_quiz_type.cli
def run(model):
    print(model.question)
    model.selection = input("Answer: ")

    return model.is_right
