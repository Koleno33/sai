from typing import List, Tuple

class Constraint:
    def __init__(self, name: str, value: float, importance: float, 
                 min_val: float = 0, max_val: float = 1):
        self.name = name
        self.value = value
        self.importance = importance
        self.min_val = min_val
        self.max_val = max_val

class Goal:
    def __init__(self, name: str, value: float, importance: float,
                 min_val: float = 0, max_val: float = 1):
        self.name = name
        self.value = value
        self.importance = importance
        self.min_val = min_val
        self.max_val = max_val

class Alternative:
    def __init__(self, name: str, constraints: List[Constraint], goals: List[Goal]):
        self.name = name
        self.constraints = constraints
        self.goals = goals

