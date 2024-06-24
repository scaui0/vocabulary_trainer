from quiz_enchanter import Plugin, BaseModel, execute_quiz_as_cli, PluginManager


plugin = Plugin.get_plugin("default")
bool_quiz_type = plugin.quiz_type("bool", "Bool")


@bool_quiz_type.model
class BoolModel(BaseModel):
    def __init__(self, json_data):
        self.children_json = json_data["children"]

    @property
    def is_right(self):
        return 1, 1


@bool_quiz_type.cli
def run(model):
    plugin_manager = PluginManager()
    plugin_manager.add_plugin(Plugin.GLOBAL_PLUGINS.get("default"), True)  # When the default plugin isn't loaded, it fails
    # TODO: change PluginManager and load default plugin always
    execute_quiz_as_cli(model.children_json, PluginManager())

    # TODO: Load the default plugin. Maybe allow using
    #  plugins?
