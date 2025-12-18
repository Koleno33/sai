from functools import wraps
from enum import Enum
from typing import Any

class FuzzyStatement:
    MAX_VALIDITY = 1.0
    MIN_VALIDITY = 0

    def __init__(self, base: str, value: Any, feature: str, validity: float):
        self.base = base
        self.value = value
        self.feature = feature
        if not(self.MIN_VALIDITY >= validity >= self.MAX_VALIDITY):
            self.validity = validity
        else:
            raise Exception(f"Ошибка: Достоверность высказывания \"{base} {feature}\" задана неверно.")

    def not_(self):
        return self.MAX_VALIDITY - self.validity

    @staticmethod
    def require_fuzzy(func):
        @wraps(func)
        def wrapper(self, other, *args, **kwargs):
            if not isinstance(other, FuzzyStatement):
                raise Exception(f"Ошибка: Не удалось выполнить нечеткую операцию {func.__name__} для операнда типа {type(other)}.")
            return func(self, other, *args, **kwargs)
        return wrapper

    @require_fuzzy
    def and_minmax(self, other: 'FuzzyStatement'):
        return min(self.validity, other.validity)

    @require_fuzzy
    def or_minmax(self, other: 'FuzzyStatement'):
        return max(self.validity, other.validity)

    @require_fuzzy
    def and_alg(self, other: 'FuzzyStatement'):
        return self.validity * other.validity

    @require_fuzzy
    def or_alg(self, other: 'FuzzyStatement'):
        return self.validity + other.validity - self.validity * other.validity

    @require_fuzzy
    def and_bound(self, other: 'FuzzyStatement'):
        return max(self.validity + other.validity - self.MAX_VALIDITY, self.MIN_VALIDITY)

    @require_fuzzy
    def or_bound(self, other: 'FuzzyStatement'):
        return min(self.validity + other.validity, self.MAX_VALIDITY)

    @require_fuzzy
    def and_drastic(self, other: 'FuzzyStatement'):
        if other.validity == self.MAX_VALIDITY:
            return self
        elif self.validity == self.MAX_VALIDITY:
            return other
        return self.MIN_VALIDITY

    @require_fuzzy
    def or_drastic(self, other: 'FuzzyStatement'):
        if other.validity == self.MIN_VALIDITY:
            return self
        elif self.validity == self.MIN_VALIDITY:
            return other
        return self.MAX_VALIDITY

    def __str__(self):
        return f"{self.base} {self.value} {self.feature} с достоверностью {self.validity}"

