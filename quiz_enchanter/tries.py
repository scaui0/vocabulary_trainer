import operator
from numbers import Number


class Tries:
    """A class representing tries and wrong tries"""

    def __init__(self, right_tries, wrong_tries):
        self.right_tries = right_tries
        self.wrong_tries = wrong_tries

    @property
    def quote(self):
        if total := self.total_tries != 0:
            return (self.right_tries / total) * 100
        else:
            return 0

    @property
    def total_tries(self):
        return self.right_tries + self.wrong_tries

    @classmethod
    def from_json(cls, json_data):
        """Load Tries from json"""
        return cls(json_data["right_tries"], json_data["wrong_tries"])

    @property
    def json(self):
        """Convert Tries to json"""
        return dict(
            right_tries=self.right_tries,
            wrong_tries=self.wrong_tries
        )

    @staticmethod
    def _compare_helper(func):
        def helper(self, other):
            if isinstance(other, Tries):
                return func(self.quote, other.quote)
            else:
                return NotImplemented

        return helper

    __lt__ = _compare_helper(operator.lt)
    __le__ = _compare_helper(operator.le)
    __eq__ = _compare_helper(operator.eq)
    __ne__ = _compare_helper(operator.ne)
    __gt__ = _compare_helper(operator.gt)
    __ge__ = _compare_helper(operator.ge)

    @staticmethod
    def _arithmetic_helper_with_two_states(operation_func):
        def helper(self, other):
            if isinstance(other, Tries):
                return Tries(operation_func(self.right_tries, other.right_tries),
                             operation_func(self.wrong_tries, other.wrong_tries))
            else:
                return NotImplemented

        return helper, helper  # For both directions

    __add__, __radd__ = _arithmetic_helper_with_two_states(operator.add)
    __sub__, __rsub__ = _arithmetic_helper_with_two_states(operator.sub)

    @staticmethod
    def _arithmetic_helper_operation_with_numbers(operation_func):
        def helper(self, other):
            if isinstance(other, Number):
                return Tries(operation_func(self.right_tries, other),
                             operation_func(self.wrong_tries, other))
            else:
                return NotImplemented

        return helper, helper

    __mul__, __rmul__ = _arithmetic_helper_operation_with_numbers(operator.mul)
    __truediv__, __rtruediv__ = _arithmetic_helper_operation_with_numbers(operator.truediv)
    __floordiv__, __rfloordiv__ = _arithmetic_helper_operation_with_numbers(operator.floordiv)
    __mod__, __rmod__ = _arithmetic_helper_operation_with_numbers(operator.mod)

    @property
    def reciprocal(self):
        try:
            return 1 / self.quote
        except ZeroDivisionError:
            return 1

    def __str__(self):
        return f"Tries: {self.right_tries}/{self.total_tries}"

    def __repr__(self):
        right_tries = self.right_tries
        wrong_tries = self.wrong_tries
        return f"{self.__class__.__name__}({right_tries=}, {wrong_tries=})"
