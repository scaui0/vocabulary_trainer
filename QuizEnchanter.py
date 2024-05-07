#!usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path

from quiz_enchanter import PluginManager, execute_quiz_as_cli_from_quiz_file

CURRENT_PATH = Path(__file__).parent

parser = ArgumentParser("QuizEnchanter", description="A quiz program")
parser.add_argument("file", nargs='?', help="optional, absolute path to a quiz file")

args = parser.parse_args()

file_argument = args.file
if file_argument is None:
    quiz_name = input("Quiz file (in quizzes folder): ")
    file_argument = CURRENT_PATH / f"quizzes/{quiz_name}"


file = Path(file_argument)
plugin_folders = [CURRENT_PATH / "quiz_enchanter/extensions/default_extension"]

if file.is_dir():
    quiz_path = file / "quiz.json"

    plugin_main_path = file / "plugins"
    if plugin_main_path.exists():
        plugin_folders += plugin_main_path.iterdir()
else:
    quiz_path = file


for plugin_path in plugin_folders:
    PluginManager.plugin_from_main_folder(plugin_path)


if quiz_path.exists():
    execute_quiz_as_cli_from_quiz_file(quiz_path)
else:
    print(f"No quiz found at {quiz_path}!")
