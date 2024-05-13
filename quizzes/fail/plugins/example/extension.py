from quiz_enchanter import Plugin, EmptyModel, InvalidJSONDataError

plugin = Plugin("fail", "Fail")

example_quiz_type = plugin.quiz_type("fail", "Fail")


@example_quiz_type.model
class Model(EmptyModel):
    def __init__(self, json_data):
        super().__init__(json_data)
        if question := json_data.get("question"):
            self.question = question
        else:
            raise InvalidJSONDataError("Missing field 'question'!")
