# Approximation task

from statements.fuzzyset import FuzzyTriangle
from statements.statement import FuzzyStatement


class Rule:
    def __init__(self, conditions, function):
        self.conditions = conditions # (FuzzyTriangle, name)
        self.function = function

    def resolve(self, inputs):
        activations = []
        
        for triangle, name in self.conditions:
            if name not in inputs:
                raise ValueError(f"Error: No value for '{name}'")
            
            value = inputs[name]
            member = triangle.resolve(value)
            activations.append(member)
        
        return min(activations) if activations else 0.0


class SugenoSystem:
    def __init__(self):
        self.rules = list() # [Rule]

    def add_rule(self, conditions, function):
        rule = Rule(conditions, function)
        self.rules.append(rule)

    def resolve(self, inputs):
        # сам нечеткий вывод
        numerator = 0.0
        denominator = 0.0

        for rule in self.rules:
            activation = rule.resolve(inputs)
            value = rule.function(inputs)

            numerator += activation * value
            denominator += activation

        if denominator == 0.0:
            return 0.0
        
        return numerator / denominator
    
    def resolve_mult(self, few_inputs):
        # нечеткий вывод для нескольких
        return [self.resolve(inputs for inputs in few_inputs)] 


