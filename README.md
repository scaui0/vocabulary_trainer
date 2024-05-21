# QuizEnchanter

## General Information
* Version: 1.0

* GitHub: https://www.github.com/scaui0/QuizEnchanter
* Python version: 3.11, 3.12 or 3.13

### Fun Fact
* Initially designed as a vocabulary trainer.

### Author
_Scaui ([scaui0 on GitHub](https://www.github.com/scaui0)) is the developer of this project.

## Installation
1. Open [QuizEnchanter on GitHub](https://www.github.com/scaui0/QuizEnchanter) in your favorite browser.
2. Click on the green button and select "Download ZIP".
3. Navigate to your download folder; then extract the downloaded ZIP file.
4. Download Python from the [official website](https://www.python.org/downloads/) and follow the installation instructions for your operating system.
5. Open the command line on your computer. On Windows, you can do this by searching for and opening `cmd`.
6. Use the `cd` command to navigate inside the extracted folder.
7. Execute the following command to install all required packages: `pip install -r requirements.txt`. 
   If it fails, try `python -m pip install -r requirements.txt` instead.
8. To run the project, use `python QuizEnchanter.py`.
   If you need arguments, you can add it. For more information see [Command-Line Interface](#command-line-interface).
9. Then you will be asked which quiz file dou want to run. You can use one of these default quizzes:
   * `example.json`
   * `test.json`
   * `geography.json`
   * `example_plugin` (not `.json`!)


## Command-Line Interface
The command-line interface for QuizEnchanter is as follows:
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
DO you want to create your own quizzes?
Let's do this!

Here is a step-by-step guide:
1. Create a JSON file with a .json extension.
2. If you're not familiar with JSON, read this guide: [JSON guide](https://www.json.org/json-en.html).
3. First, you need to give it a name. Then, the file will look like this:
   ```json
   {
     "name": "Example Quiz"
   }   
   ```
4. Then you need to add some questions.
   A question is an object in the `quizzes` array.
   You need to add a `type` to each question.
   Then you can add some more information, that will be passed to the appropriate quiz type.

   There are five builtin quiz types you can use:

   | Quiz Type    | Short Description                             |
   |--------------|-----------------------------------------------|
   | `select`     | Select one from a list of options.            |
   | `match`      | User's answer is a string.                    |
   | `bool`       | The user decides whether a statement is true. |
   | `datetime`   | A time in ISO 8601.                           |
   | `timeperiod` | A time period in ISO 8601.                    |

   More information, like JSON fields for every builtin quiz type,
   can be found in [Builtin Quiz Types](#builtin-quiz-types).

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
         "question": "The first is correct!",
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
   It isn't very useful, but it is still an example.

5. Move your quiz into the `quizzes` folder, 
   run the `QuizEnchanter.py` file with Python and write the name of your quiz file.


## Builtin Quiz Types

### Short Descriptions

| Quiz Type    | Short Description                             |
|--------------|-----------------------------------------------|
| `select`     | Select one from a list of options.            |
| `match`      | User's answer is a string.                    |
| `bool`       | The user decides whether a statement is true. |
| `datetime`   | A time in ISO 8601.                           |
| `timeperiod` | A time period in ISO 8601.                    |


### Long Descriptions


* `select`:
  This quiz type allows creating multiple-choice questions with predefined answer options.
   
  | Argument | Information                                                      | Required |
  |----------|------------------------------------------------------------------|----------|
  | question | The question                                                     | true     |
  | options  | Array of strings                                                 | true     |
  | right    | Right index or right indexes as array. All indexes start from 0! | false    |

  Example:
  
    ```json
    {
      "type": "select",
      "question": "Which mountain the the highest one?",
      "options": ["Fuji", "Mount Everest", "Zugspitze"],
      "right": 1
    }
    ```
   
* `match`:
  The answer to the question is a string.
   
  | Argument            | Information                                  | Required | Default                    | Cannot used with |
  |---------------------|----------------------------------------------|----------|----------------------------|------------------|
  | question            | The question                                 | true     |                            |                  |
  | strip_start_and_end | Strip whitespaces around the answer          | false    | true                       |                  |
  | right               | The right answer/answers                     | false    | The answer cannot be right |                  |
  | ignore_case         | Ignore case                                  | false    | false                      |                  |
  | regex               | Answer must match the RegEx (Python-dialect) | false    | `.*` (matches all answers) |                  |

  Example without the `regex` field:
  ```json
  {
    "type": "match",
    "question": "English or German greeting, beginning with 'h'?",
    "right": ["hello", "hallo"],
    "ignore_case": true
  }
  ```
  The same example using the `regex` field:
  ```json
  {
    "type": "match",
    "question": "English or German greeting, beginning with 'h'?",
    "regex": "h[ae]llo",
    "ignore_case": true
  }
  ```

* `bool`:
  The user has to decide whether the statement is right.
      
  | Argument | Information                                      | Required |
  |----------|--------------------------------------------------|----------|
  | question | The question (actually a statement)              | true     |
  | right    | Indicates whether the question’s answer is right | true     |

  Example:
  ```json
  {
    "type": "bool",
    "question": "Mount Everest is the highest mountain on Earth.",
    "right": true
  }
  ```

   
* `datetime`:
  This quiz type asks the user for a specific date.
  This date uses the ISO 8601 format!
  Simplified that is the format: `YYYY-MM-DDThh:mm:ss`.
  If you don't need the time, you can omit it.
  The same applies to the date
  When needed, `T` is the seperator between the date and the time.
  It can only check times and dates, but not time periods!
     
  | Argument                | Information                                       | Required | Default |
  |-------------------------|---------------------------------------------------|----------|---------|
  | question                | The question                                      | true     |         |
  | right                   | The right date(s) in ISO 8601 format              | true     |         |
  | show_format_information | Shows a message about the date format to the user | false    | true    |

  Example:
  ```json
  {
    "type": "datetime",
    "question": "On which date in 2000 was Christmas?",
    "right": ["2000-12-24", "2000-12-25", "2000-12-26"]
  }
  ```
   
* `timeperiod`:
  A timeperiod in ISO 8601.
   
  | Argument | Information              | Required |
  |----------|--------------------------|----------|
  | question | The question             | true     |
  | right    | The right time period(s) | true     |

  Example:
  ```json
  {
    "type": "timeperiod",
    "question": "How long is the period between St. Nicholas and Christmas?",
    "right": ["P18D", "P19D"]
  }
  ```


## Plugin Development
Not enough quiz types? Let's create your own plugin and define your own quiz types!

A plugin is a folder containing at least one file: a configuration file `extension.json`.
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
6. Fill the referenced Python files with your plugin content!
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
    This is more comfortable than the other option.
   
   * The other way is to use `plugin.register_quiz_type(id, name, model, cli)`.
   
   After registration, you can use your quiz type in quiz files.
   Set the `type` to your quiz type's id and fill the other parameters for your quiz type.
   All parameters are passed to your model.
   
   The model class is a class inhered by `BaseModel` and its `__init__` expects one argument:
   a `dict` filled with information from the quiz file.
   The model should define a property called `is_right`.
   Otherwise, the model is always right.
   You don't have to define a model class.
   If you don't, the `cli`'s `model` parameter will be a dict, filled with information from the JSON file.
   
   The `cli` function expects one argument `model` and return a boolean,
   which indicates whether the result is correct.


### An Example Plugin

This example plugin can be found under the name `example_plugin` in the `quizzes` folder.
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
Since there are plugins needed for the quiz, we need to place it into a folder and name the quiz file `quiz.json`.
Next to `quiz.json`, we must create a folder `plugins` and place our plugin inside it.
Then start the QuizEnchanter.py and write `example`!

If you want, create more complex quizzes and plugins!
Good luck!