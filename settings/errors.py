class CorrectionError(BaseException):
    """Raised when value correction fails."""


class InvalidValueError(BaseException):
    """Raised ehen value is invalid and cannot be corrected"""

    def __init__(self, value, cls=None):
        self.cls = cls
        self.value = value

    def __str__(self):
        return f"{self.value !r} is an invalid value for {self.cls.__class__.__name__}"
