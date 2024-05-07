# QuizEnchanter

## General Information
* Version: 1.0

* GitHub: https://www.github.com/scaui0/QuizEnchanter
* Python version: this project needs Python 3.11, 3.12 or 3.13!

### Author
_Scaui (scaui0 on GitHub) is the developer of this project.

## Installation
### Using GitHub
1. Open https://www.github.com/scaui0/QuizEnchanter in your favorite browser
2. Click on the green button and on "Download ZIP"
3. Switch in your Download folder right-click the zip-file and unpack it
4. If python isn't installed, you need to install it. You need Python 3.11 or newer


## Command-Line Interface
This program has a command-line interface:
```
usage: QuizEnchanter [-h] [file]

A quiz program

positional arguments:
  file        optional, absolut path to a quiz file

options:
  -h, --help  show this help message and exit
```


## Create Quiz Files
You want to create your own quizzes?
Let's do this!

Here is a step-by-step guide:
1. Create a JSON file with a .json extension.
2. If you're not familiar with JSON, read this guide: https://www.json.org/json-en.html
3. First, you need to give it a name. Then the file will look like this:
    ```json
    {
      "name": "Example Quiz"
    }
    ```
4. Then you need to add some questions.
   A question is an object in the `quizzes` array.
   You need to add a `type` to each question.
   Then you can add some more information which will be passed to the appropriate quiz type.
   
   There are three basic quiz types you can use:

    | type name | arguments                                                                                             |
    |-----------|-------------------------------------------------------------------------------------------------------|
    | `select`  | options: array of string <br/>right: right index of options, starting from 0! <br/>question: question |
    | `bool`    | question: question (actually a statement)<br/> right: bool                                            |
    | `match`   | question: question<br/> right: string<br/> strip_start_and_end: strip whitespaces around the answer   |
   
   Here is a short example:
   ```
   {
      "name": "Test Quizzes",
      "quizzes": [
        {
          "type": "match",
          "question": "Please answer 'HI'!",
          "right": "HI"
        },
        {
          "type": "bool",
          "question": "This is true!",
          "right": true
        },
        {
          "type": "select",
          "question": "The first is the right!",
          "options": ["1", "2", "3", "4"],
          "right": 0
        }
      ]
    }
   ```
   It isn't very useful, but it's still an example.
5. Move you quiz in the `quizzes` folder, 
   run the `QuizEnchanter.py` file with Python and write the name of your quiz file.



## Plugin Development
Not enough quiz types? Let's create your own plugin and define your own Quit-Types!

A plugin is a folder containing at least one file: A configuration file `extension.json`.
This plugin can't register quiz types.
If you want to register quiz types (why else would you create a plugin?), you must have at least one Python file,
which is linked in the `files` array of the configuration file.

Here is a step-by-step guide:
1. Create a folder that should ideally have the name of the plugin.
2. Create the plugin main file, which is a Python file.
3. Copy the following template inside a new `extension.json` file, which is in the main folder:
    ```json
    {
      "name": "",
      "id": "",
      "files": []
    }
    ```
4. Fill the name and the id. The id should be unique!
5. Create a new python file in the main folder and refer it in the `file` field of the `extension.json` file.
6. Fill the referred python files with your plugin content!
   When you create quiz types, you need to have a plugin object.
   Create it like this:
   ```python
   from quiz_enchanter import Plugin
   plugin = Plugin("id", "Name")
   ```
   The id needs to be the id from the config file.
   When you need this plugin in another file to register more quiz types,
   you can use `Plugin.get_plugin("id")`, where id is your plugin's id.
   
   There are two ways to register quiz types:
   * Use decorators.
    `quiz_type = plugin.quiz_type("id", "Name")` creates an empty quiz type.
    To register model or command-line interfaces, use their decorators.
    They're called `model` and `cli`.
    Model is a class, inhered by `BaseModel` and shout defines the property `is_right`.
    This is more comfortable than the other option.
   
   * The other way is to use `plugin.register_quiz_type(id, name, model, cli)`.
   
   After registration, you can use your quiz type in quiz files.
   Set the `type` to your quiz type id and fill the other parameters for your quiz type.
   All parameters are given to your model.
   
   The model class' `__init__` must expect one argument: a `dict` filled with information from the quiz file.
   The model shout defines a property `is_right`.
   
   The `cli` function must expect one argument `model` and return a boolean,
   which indicates whether the result is right.


### An example Plugin

This example plugin can be found under the name `example` in the `quizzes` folder.
This example Plugin has the following structure:
```
example_plugin/
   extension.json
   example.py
```
The `extension.json` has the following content:
```json
{
  "name": "Example Plugin!",
  "id": "example",
  "files": ["example.py"]
}
```
The `example.py`:

```python
from quiz_enchanter import Plugin, BaseModel


plugin = Plugin("example", "Example plugin")  # The id must match the id from the config file
example_quiz_type = plugin.quiz_type("example", "Example quiz type")


@example_quiz_type.model
class ExampleModel(BaseModel):
   def __init__(self, json_data):
      self.question = json_data["question"]
   
   
@example_quiz_type.cli
def run(model):
    input(model.question)

    return True
```

To test it, we need to create a quiz.
Because there are plugins needed for the quiz, we need to put it into a folder and name the quiz file `quiz.json`.
Next to `quiz.json`, we must create a folder `plugins` and put our plugin inside it.
Then start the QuizEnchanter.py and write `example`!

If you want, you can create more complex quizzes and plugins!
Good luck!