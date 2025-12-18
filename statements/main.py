import fuzzyset
from statement import FuzzyStatement
from fuzzyset import FuzzySet

def statements():
    fs1 = FuzzyStatement("погода с температурой воздуха", 40, "жаркая", 0.7)
    fs2 = FuzzyStatement("погода с температурой воздуха", 40, "жаркая", 0.4)

    print("fs1")
    print(fs1)
    print("fs2")
    print(fs2)
    print()

    print("NOT fs1")
    print(fs1.not_())
    print("NOT fs2")
    print(fs2.not_())
    print()

    print("minmax:")
    print("fs1 AND fs2")
    print(fs1.and_minmax(fs2))
    print("fs1 OR fs2")
    print(fs1.or_minmax(fs2))
    print()

    print("alg:")
    print("fs1 AND fs2")
    print(fs1.and_alg(fs2))
    print("fs1 OR fs2")
    print(fs1.or_alg(fs2))
    print()

    print("bound:")
    print("fs1 AND fs2")
    print(fs1.and_bound(fs2))
    print("fs1 OR fs2")
    print(fs1.or_bound(fs2))
    print()

    print("drastic:")
    print("fs1 AND fs2")
    print(fs1.and_drastic(fs2))
    print("fs1 OR fs2")
    print(fs1.or_drastic(fs2))
    print()

def sets():
    fset1 = FuzzySet([
        FuzzyStatement("погода с температурой воздуха", 20, "теплая", 0.7),
        FuzzyStatement("погода с температурой воздуха", 30, "теплая", 0.9),
        FuzzyStatement("погода с температурой воздуха", 10, "теплая", 0.2),
        FuzzyStatement("погода с температурой воздуха", 10, "теплая", 0.2),
    ])
    fset2 = FuzzySet([
        FuzzyStatement("погода с температурой воздуха", 10, "теплая", 0.2),
        FuzzyStatement("погода с температурой воздуха", 15, "теплая", 0.3),
        FuzzyStatement("погода с температурой воздуха", 20, "теплая", 0.4),
    ])
    print("fuzzy set 1:")
    print(fset1)
    print("fuzzy set 2:")
    print(fset2)
    print()

    print("intersect fs1 and fs2:")
    newset1 = fset1.intersect(fset2)
    print(newset1)
    print()

    print("union fs1 and fs2:")
    newset2 = fset1.union(fset2)
    print(newset2)
    print()

