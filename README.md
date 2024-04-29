# QuizEnchanter

This project is in development! So a lot will be changed in the future!

## Information
* GitHub: https://www.github.com/scaui0/QuizEnchanter

### Author
_Scaui(also known as scaui0 on GitHub) is the developer of this project.

## Installation
### Using GitHub
1. Open https://www.github.com/scaui0/QuizEnchanter in your favorite browser
2. Click on the green button in the right-top corner and on "Download ZIP"
3. Switch in your Download folder right-click the zip-file and unpack it
4. If python isn't installed, you need to install it. You need Python 3.11 or newer


## Create Quiz-Files


### Plugin development
You want to define your own Quiz-Types? Create your own plugin and define your own Quit-Types!

To create a Plugin, follow the following step-by-step-guide:
1. Create a folder, which name is your plugin name.
2. Create the Plugin-Main-File, which is a python file.
3. Copy the following Template inside a new `extension.json` file, which is in the main-folder:
    ```
    {
      "name": "",
      "id": "",
      "file": ""
    }
    ```
4. Fill the name and the id. The id should be unique!
5. Create a new python file(.py) in the main folder and refer it in the file field of the `extension.json`-file.
6. Fill the referred python file with your plugin content!

#### An example Plugin

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
  "file": "example.py"
}
```
The `example.py`:
```python
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from quiz_enchanter import Plugin

plugin = Plugin(identifier="example")  # identifier must match that from the json-file!

@plugin.quiz_type("Text", "text")
class TextQuizType(QWidget):
    def __init__(self, text, parent=None):  # Needs to have a parameter "parent"!
        super().__init__(parent)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text, self))
        self.setLayout(layout)
    

    @classmethod
    def from_json(cls, json_data, parent=None):  # Needs parent too!
        return cls(json_data["text"], parent)
```