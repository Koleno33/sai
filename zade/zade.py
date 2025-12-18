from typing import List, Tuple

class Constraint:
    def __init__(self, name: str, value: float, importance: float):
        self.name = name
        self.value = value
        self.importance = importance

class Goal:
    def __init__(self, name: str, value: float, importance: float):
        self.name = name
        self.value = value
        self.importance = importance

class Alternative:
    def __init__(self, name: str, constraints: List[Constraint], goals: List[Goal]):
        self.name = name
        self.constraints = constraints
        self.goals = goals

