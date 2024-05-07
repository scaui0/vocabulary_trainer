from quiz_enchanter import Plugin, EmptyModel

plugin = Plugin.get_plugin("default")
select_quiz_type = plugin.quiz_type("select", "Select")


@select_quiz_type.model
class SelectModel(EmptyModel):
    def __init__(self, json_data):
        super().__init__(json_data)
        self.question = json_data["question"]
        self.options = json_data["options"]
        self.right = json_data["right"]

        self.selected_index = None

    @property
    def is_right(self):
        return self.selected_index == self.right


@select_quiz_type.cli
def run(model):
    print(model.question)

    for i, option in enumerate(model.options):
        print(f"[{i+1}]", option)  # +1 because it starts from 1

    while True:
        selection = input("Select index: ")
        try:
            model.selected_index = int(selection)-1  # -1 because in quiz creation it's easier to be written
            # by the user
            break
        except ValueError:
            pass

    return model.is_right
