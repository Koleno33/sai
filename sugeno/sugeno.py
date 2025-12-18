# Approximation task

from typing import Callable, List, Tuple
import math


class InputRange:
    def __init__(self, minimal: float, maximum: float):
        self.minimal = minimal
        self.maximum = maximum


class Rule:
    def __init__(self, input_range: InputRange, function: Callable):
        self.input_range = input_range # диапазон возможных значений
        self.function    = function
    
    def calculate(self, x):
        return self.function(x)


class RuleLine:
    def __init__(self, number: float, rules: List[Rule], z: float):
        self.number = number   # порядковый номер ряда правил
        self.rules  = rules
        self.z      = z

    def calculate(self, input_vals):
        calc_results = []
        for index, x in enumerate(input_vals):
            cr = self.rules[index].calculate(x)
            if cr is not None:
                calc_results.append(cr)

        return min(calc_results)


class Approximator:
    def __init__(self, rulelines: List[RuleLine]):
        self.rulelines  = rulelines

    def calculate(self, input_vals: Tuple):
        calc_results = []
        for index, rl in enumerate(self.rulelines):
            calc_results.append(rl.calculate(input_vals) * rl.z)

        return sum(calc_results) / len(calc_results)


def measure_service(x):
    return math.sqrt(x)

def measure_food(x):
    return math.sin(x)

def measure_service2(x):
    return x * 2 + 1

def measure_food2(x):
    return None

if __name__ == "__main__":
    rules1 = [
            Rule(InputRange(0, 10), measure_service), # service
            Rule(InputRange(1, 5), measure_food),     # food
    ]

    rules2 = [
            Rule(InputRange(0, 10), measure_service2), # service
            Rule(InputRange(1, 5), measure_food2),     # food
    ]

    rulelines = [
            RuleLine(1, rules1, 3),
            RuleLine(2, rules2, 5),
    ]

    input_vals = (
        3, 8
    )

    app = Approximator(rulelines)
    res = app.calculate(input_vals)

    print(f"Result: {res:.2f}")


