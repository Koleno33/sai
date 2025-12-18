from zade import Alternative, Constraint, Goal
from alts import qual_alts, comp_alts
from typing import List, Tuple

def print_alt(alt: Alternative):
    print("---Best alternative---")
    print(f"Name: {alt.name}")

def print_alts(alts: List[Alternative]):
    print("---All alternatives---")
    for alt in alts:
        print()
        print("Alternative name: ", alt.name)
        print("*** Goals: ***")

        print(f"|{"Название":^20}|{"Значение":^20}|{"Важность":^20}|")
        for goal in alt.goals:
            print(f"|{str(goal.name):^20}|{str(goal.value):^20}|{str(goal.importance):^20}|")
        print("*** Constraints: ***")
        print(f"|{"Название":^20}|{"Значение":^20}|{"Важность":^20}|")
        for constraint in alt.constraints:
            print(f"|{str(constraint.name):^20}|{str(constraint.value):^20}|{str(constraint.importance):^20}|")
        print()
    print()

def make_zade1(alts: List[Alternative]):
    best_alt_value = 0.0
    best_alt = alts[0]
    for alt in alts[1:]:
        constraints_min = min([v.value * v.importance for v in alt.constraints])
        goals_min = min([v.value * v.importance for v in alt.goals])
        new_value = min(constraints_min, goals_min)
        if new_value > best_alt_value:
            best_alt = alt
            best_alt_value = new_value

    print_alt(best_alt)

def choose(alts):
    print_alts(alts)
    make_zade1(alts)

choose(qual_alts)
