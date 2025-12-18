from statements.statement import FuzzyStatement
from functools import wraps

class FuzzySet:
    def __init__(self, statements: list['FuzzyStatement'] = list()):
        if not statements:
            self.__statements = list()
            return
        self.__statements = statements
        for s in self.__statements:
            s.base = s.base.lower()
            s.feature = s.feature.lower()
        self.__make_unique()

    def __make_unique(self):
        for first_s in self.__statements:
            for index, second_s in enumerate(self.__statements):
                if first_s is second_s:
                    continue
                if first_s.feature == second_s.feature and first_s.value == second_s.value:
                    self.__statements.remove(second_s)

    @staticmethod
    def require_fuzzy_set(func):
        @wraps(func)
        def wrapper(self, other, *args, **kwargs):
            if not isinstance(other, FuzzySet):
                raise Exception(f"Ошибка: Не удалось выполнить операцию {func.__name__} нечетких множеств для операнда типа {type(other)}.")
            return func(self, other, *args, **kwargs)
        return wrapper

    @FuzzyStatement.require_fuzzy
    def add(self, other: 'FuzzyStatement'):
        basel = other.base.lower()
        featurel = other.feature.lower()
        for s in self.__statements:
            if s.base != basel or s.feature != featurel or s.value == other.value:
                return
        self.__statements.append(other)

    @require_fuzzy_set
    def union(self, other: 'FuzzySet'):
        res = FuzzySet()
        valval = dict() # value: [fss]
        allfs = self.__statements + other.__statements

        for fs in allfs:
            if fs.value not in valval:
                valval[fs.value] = list()
            valval[fs.value].append(fs)

        for value in valval:
            fss = valval[value]
            if len(fss) > 1:
                res.add(max(fss, key=lambda fs: fs.validity))
            else:
                res.add(fss[0])

        return res

    @require_fuzzy_set
    def intersect(self, other: 'FuzzySet'):
        res = FuzzySet()
        valval = dict() # value: [fss]
        allfs = self.__statements + other.__statements

        for fs in allfs:
            if fs.value not in valval:
                valval[fs.value] = list()
            valval[fs.value].append(fs)

        for value in valval:
            fss = valval[value]
            if len(fss) > 1:
                res.add(min(fss, key=lambda fs: fs.validity))

        return res
    
    def __str__(self):
        res = ""
        for s in self.__statements:
            res += str(s)
            res += '\n'
        res = res[:-1]
        return res


class FuzzyTriangle:
    def __init__(self, statements: list['FuzzyStatement']):
        if len(statements) != 3:
            raise Exception("Задан не треугольник")
        count_one, count_zero = 0, 0
        self.__statements = list()
        for s in statements:
            if s.validity == 1:
                self.__statements.append(s)
                count_one += 1
            elif s.validity == 0:
                self.__statements.append(s)
                count_zero += 1
        if count_one > 2 or count_zero > 2:
            raise Exception("Неверно задан треугольник")
        self.__statements.sort(key=lambda x: x.value)
        self.b1 = self.__statements[0]
        self.t = self.__statements[1]
        self.b2 = self.__statements[2]
        # print("Левая", self.b1)
        # print("Средняя", self.t)
        # print("Правая", self.b2)
        # print()

    def resolve(self, value):
        validity = 0
        if value < self.b1.value or value > self.b2.value:
            #raise Exception("Точка вне границ заданного треугольника")
            return validity
        # print("found", value, "between", self.b1.value, "and", self.b2.value)
        # k = ( self.b1.validity / self.b1.value - self.t.validity ) / ( 1 + self.b2.validity )
        # b = self.t.validity - k * self.b2.value
        if value >= self.t.value:
            if self.b2.validity == 1.0:
                return 1.0
            # print("b2 validity", self.b2.validity)
            k = 1 / (self.t.value - self.b2.value)
            b = -k * self.b2.value
        else:
            if self.b1.validity == 1.0:
                return 1.0
            k = 1 / (self.t.value - self.b1.value)
            b = -k * self.b1.value
        # print("k = ", k)
        # print("b = ", b)
        validity = k * value + b
        return validity


class FuzzyTrapezoid:
    def __init__(self, statements: list['FuzzyStatement']):
        if len(statements) != 3:
            raise Exception("Задана не трапеция")
        count_one, count_zero = 0, 0
        self.__statements = list()
        for s in statements:
            if s.validity == 1:
                self.__statements.append(s)
                count_one += 1
            elif s.validity == 0:
                self.__statements.append(s)
                count_zero += 1
        if count_one > 3 or count_zero > 3:
            raise Exception("Неверно задана трапеция")
        self.__statements.sort(key=lambda x: x.value)
        self.b1 = self.__statements[0]
        self.t1 = self.__statements[1]
        self.t2 = self.__statements[2]
        self.b2 = self.__statements[3]
        # print("Левая нижняя", self.b1)
        # print("Левая верхняя", self.t1)
        # print("Правая верхняя", self.t2)
        # print("Правая нижняя", self.b2)
        # print()

    def resolve(self, value):
        validity = 0

        if value >= self.t1.value and value <= self.t2.value:
            return 1.0
        elif value <= self.b2.value:
            if self.b2.validity == 1.0:
                return 1.0
            k = 1 / (self.t2.value - self.b2.value)
            b = -k * self.b2.value
        elif value >= self.b1.value:
            if self.b2.validity == 1.0:
                return 1.0
            k = 1 / (self.t1.value - self.b1.value)
            b = -k * self.b1.value
        else:
            return 0.0

        # print("found", value, "between", self.b1.value, "and", self.b2.value)

        # print("k = ", k)
        # print("b = ", b)
        validity = k * value + b
        return validity

