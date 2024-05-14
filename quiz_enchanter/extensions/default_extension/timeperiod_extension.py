from datetime import datetime, timedelta

from isodate import parse_duration

from quiz_enchanter import Plugin, BaseModel

plugin = Plugin.get_plugin("default")
date_period_quiz_type = plugin.quiz_type("timeperiod", "TimePeriod")


@date_period_quiz_type.model
class TimePeriodModel(BaseModel):
    def __init__(self, json_data):
        self.question = json_data["question"]

        self.right = parse_duration(json_data["right"])

        self.selection = None

    @property
    def is_right(self):
        return self.selection == self.right


@date_period_quiz_type.cli
def run(model):
    print(model.question)

    while True:
        answer = input("Answer: ")
        try:
            model.selection = parse_duration(answer)
            break
        except ValueError:
            continue

    return model.is_right
