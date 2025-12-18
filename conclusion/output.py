class Rule:
    def __init__(self, left: list, right: list):
        self.left = left
        self.right = right

class DirectOutput:
    CONSTRAINT = 1000

    def __init__(self, facts, rules):
        self.facts = facts
        self.rules = rules

    def can_output(self, fact):
        for rule in self.rules:
            if fact in rule.right and set(rule.left).issubset(set(self.facts)) and (fact not in self.facts):
                return True
        return False

    def make_output(self):
        right_parts = set(rule.right[0] for rule in self.rules)
        iterations = 0
        while not right_parts.issubset(set(self.facts)):
            for rule in self.rules:
                if self.can_output(rule.right[0]):
                    print(f"New fact added: {rule.left} -> {rule.right}")
                    self.facts.append(rule.right[0])
            if iterations == self.CONSTRAINT:
                print(f"Can't output {set(right_parts) - set(self.facts)}")
                break
            iterations += 1
        print(f"Total iterations: {iterations}\n")


class ReversedOutput:
    def __init__(self, facts, rules):
        self.facts = facts.copy()
        self.rules = rules
        self.new_facts = list()

    def can_output(self, fact):
        if fact in self.facts:
            return True

        good_rules = [rule for rule in self.rules if fact in rule.right]

        for rule in good_rules:
            all_left_good = True
            for left_fact in rule.left:
                if not self.can_output(left_fact):
                    all_left_good = False
                    break

            if all_left_good:
                if fact not in self.facts:
                    self.facts.append(fact)
                    self.new_facts.append(fact)
                    print(f"New fact added: {fact} (from rule {rule.left} -> {rule.right})")
                return True

        return False

    def make_output(self):
        self.new_facts = list()
        for rule in self.rules:
            if not self.can_output(rule.right[0]):
                print(f"Can't ouput {rule.right}")
        return self.new_facts


def main():
    print("---Start direct output---")

    do = DirectOutput(
            facts = ["A", "E", "G", "C", "H", "B"],
            rules = [
                Rule(["F", "B"],["Z"]),
                Rule(["C", "D"],["F"]),
                Rule(["A"],["D"]),
                Rule(["X", "Y"],["M"])])
    do.make_output()

    print("---Start reversed output---")

    ro = ReversedOutput(
            facts = ["A", "E", "G", "C", "H", "B"],
            rules = [
                Rule(["F", "B"],["Z"]),
                Rule(["C", "D"],["F"]),
                Rule(["A"],["D"]),
                Rule(["X", "Y"],["M"])])
    ro.make_output()

