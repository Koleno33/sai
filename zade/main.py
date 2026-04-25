import alts
from zade import Alternative, Constraint, Goal
from typing import List, Tuple, Dict

def print_alt(alt: Alternative):
    print("---Лучшие альтернативы---")
    print(f"Name: {alt.name}")

def print_alts(alts: List[Alternative]):
    print("---Все альтернативы---")
    for alt in alts:
        print()
        print("Название альтернативы: ", alt.name)
        print("*** Goals: ***")
        print(f"|{'Название':^26}|{'Значение':^20}|{'Важность':^20}|")
        for goal in alt.goals:
            print(f"|{str(goal.name):^26}|{str(goal.value):^20}|{str(goal.importance):^20}|")
        print("*** Constraints: ***")
        print(f"|{'Название':^26}|{'Значение':^20}|{'Важность':^20}|")
        for constraint in alt.constraints:
            print(f"|{str(constraint.name):^26}|{str(constraint.value):^20}|{str(constraint.importance):^20}|")
        print()
    print()

def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 0.5
    return (value - min_val) / (max_val - min_val)

def make_zade(alts: List[Alternative]) -> Tuple[Alternative, Dict[str, float]]:
    """
    Выполняет расчёт по методу Беллмана-Заде.
    Возвращает кортеж: (лучшая альтернатива, словарь {имя_альтернативы: итоговая_оценка})
    """
    best_alt = None
    best_score = -float('inf')
    scores = {}

    for alt in alts:
        memberships = []

        for constraint in alt.constraints:
            membership = constraint.value * constraint.importance
            memberships.append(membership)

        for goal in alt.goals:
            membership = goal.value * goal.importance
            memberships.append(membership)

        alt_score = min(memberships) if memberships else 0
        scores[alt.name] = alt_score

        print(f"\n{alt.name}")
        print(f"  Минимальное значение: {alt_score:.4f}")
        print(f"  Все взвешенные параметры: {[f'{m:.3f}' for m in sorted(memberships)]}")

        if alt_score > best_score:
            best_score = alt_score
            best_alt = alt

    print(f"\n{'='*60}")
    print(f"Лучшая альтернатива: {best_alt.name}")
    print(f"Итоговая оценка: {best_score:.4f}")
    return best_alt, scores

def choose(alts):
    print_alts(alts)
    best_alt, _ = make_zade(alts)   # оценки не нужны при консольном вызове
