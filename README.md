# QuizEnchanter

## General Information
* Version: 1.0

* GitHub: https://www.github.com/scaui0/QuizEnchanter
* Python version: 3.11, 3.12 or 3.13

### Fun Fact
* This program has been going to be a vocabulary trainer.

### Author
_Scaui (scaui0 on GitHub) is the developer of this project.

## Installation
### Using GitHub
1. Open https://www.github.com/scaui0/QuizEnchanter in your favorite browser.
2. Click on the green button and on "Download ZIP".
3. Navigate to your download folder; then extract the downloaded ZIP file.
4. If not yet done, you need to install Python version 3.11 or newer.


## Command-Line Interface
This program has a command-line interface:
```
usage: QuizEnchanter [-h] [-d] [file]

A quiz program

positional arguments:
  file         optional, absolute path to a quiz file

options:
  -h, --help   show this help message and exit
  -d, --debug  print debug messages
```


## Create Quiz Files
You want to create your own quizzes?
Let's do this!

Here is a step-by-step guide:
1. Create a JSON file with a .json extension.
2. If you're not familiar with JSON, read this guide: https://www.json.org/json-en.html.
3. First, you need to give it a name. Then the file will look like this:
    ```json
    {
      "name": "Example Quiz"
    }
    ```
4. Then you need to add some questions.
   A question is an object in the `quizzes` array.
   You need to add a `type` to each question.
   Then you can add some more information, that will be passed to the appropriate quiz type.

   There are four basic quiz types you can use:
   
   * `select`:
     This quiz type allows creating multiple-choice questions with predefined answer options.
   
     | Argument | Information                                                      |
     |----------|------------------------------------------------------------------|
     | question | The question                                                     |
     | options  | Array of strings                                                 |
     | right    | Right index or right indexes as array. All indexes start from 0! |
   
   * `match`:
     The answer of the question is a string.
   
     | Argument            | Information                                  |
     |---------------------|----------------------------------------------|
     | question            | The question                                 |
     | strip_start_and_end | Strip whitespaces around the answer          |
     | right               | The right answer/answers                     |
     | ignore_case         | Ignore case                                  |
     | regex               | Answer must match the RegEx (Python-dialect) |

   * `bool`:
     The user has to decide whether the statement is right.
      
     | Argument | Information                                      |
     |----------|--------------------------------------------------|
     | question | The question (actually a statement)              |
     | right    | Indicates whether the question’s answer is right |
   
   * `datetime`:
     This quiz type asks the user for a specific date.
     This date uses the ISO 8601 format!
     Simplified that is the format: `YYYY-MM-DDThh:mm:ss`.
     In this case, the `T` is the seperator between the date and the time.
     It can only check times and dates, but no time deltas!
     
     | Argument                | Information                                                        |
     |-------------------------|--------------------------------------------------------------------|
     | question                | The question                                                       |
     | right                   | The right date(s) in ISO 8601 format                               |
     | show_format_information | Shows a message about the date format to the user (default `true`) |
   
   * `timeperiod`:
     A timeperiod in ISO 8601.
   
     | Argument | Information           |
     |----------|-----------------------|
     | question | The question          |
     | right    | The right time period |

   Here is a short example:
   ```json
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
       },
       {
         "type": "date",
         "question": "Please answer 2000-01-01!",
         "right": "2000-01-01",
         "show_format_information": false
       }
     ]
   }
   ```
   It isn't very useful, but it's still an example.

5. Move your quiz into the `quizzes` folder, 
   run the `QuizEnchanter.py` file with Python and write the name of your quiz file.


## Plugin Development
Not enough quiz types? Let's create your own plugin and define your own quiz types!

A plugin is a folder containing at least one file: A configuration file `extension.json`.
This simple plugin cannot register quiz types.
If you want to register quiz types (why else would you create a plugin?), you must have at least one Python file,
which is linked in the `files` array of the configuration file.

The builtin quiz types are defined by the `default` plugin.

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
5. Create a new python file in the main folder and specify it in the `file` field of the `extension.json` file.
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
    They are called `model` and `cli`.
    Model is a class, inhered by `BaseModel` and should define the property `is_right`.
    This is more comfortable than the other option.
   
   * The other way is to use `plugin.register_quiz_type(id, name, model, cli)`.
   
   After registration, you can use your quiz type in quiz files.
   Set the `type` to your quiz type id and fill the other parameters for your quiz type.
   All parameters are passed to your model.
   
   The model class' `__init__` expects one argument: a `dict` filled with information from the quiz file.
   The model should define a property `is_right`.
   Otherwise, the model is always right.
   
   The `cli` function expects one argument `model` and return a boolean,
   which indicates whether the result is right.


### An example Plugin

This example plugin can be found under the name `example` in the `quizzes` folder.
This example plugin has the following structure:
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
`example.py`:

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
Because there are plugins needed for the quiz, we need to place it into a folder and name the quiz file `quiz.json`.
Next to `quiz.json`, we must create a folder `plugins` and place our plugin inside it.
Then start the QuizEnchanter.py and write `example`!

If you want, create more complex quizzes and plugins!
Good luck!