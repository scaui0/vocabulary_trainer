# Help for settings
## Start using
### Little example

```python
setting = BooleanSetting(True, "Test", "test")
setting.value = False
print(setting.value)  # False
```

### Correct values
IWhen you would run this example, you'll see an Exception:
```python
setting = IntegerSetting(1, "Int", "int", "Foo")
setting.value = 5
print(setting.value)
setting.value = "6"  # Invalid, will raise InvalidValueException
print(setting.value)
```
It's because the value in invalid and can't be corrected.
But you can add the correct_values parameter. 
If this parameter is True, it will try to correct your value.
```python
setting = IntegerSetting(1, "Int", "int", "Foo", True)
setting.value = 5
print(setting.value)
setting.value = "6"  # It isn't invalid again
print(setting.value)  # The value was converted into a str
```

### Write our own Settings
When you want to write our own setting, you'll see that it's very easy:
```python
class MySetting(Setting):
    def validate(self, value) -> bool:
        return value.islower() if isinstance(value, str) else False

    def correct(self, value) -> Any:
        if isinstance(value, str):
            return value.lower()
        else:
            raise CorrectionError
```
Now you can use this setting like others. The value will be corrected because the correct_values is True
```python
setting = MySetting("hello, world", "Foo", "bar", True)
# The last parameter specificed that the value should be corrected

settings.value = "SPAM"  # will be corrected
print(settings.value)
```