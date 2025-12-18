from sugeno import SugenoSystem, Rule
from statements.fuzzyset import FuzzyTriangle
from statements.statement import FuzzyStatement

def create_approximation_system():
    low_x = FuzzyTriangle([
        FuzzyStatement("x", 0, "Низкий", 0.0),
        FuzzyStatement("x", 2, "Низкий", 1.0),
        FuzzyStatement("x", 5, "Низкий", 0.0)
    ])
    
    medium_x = FuzzyTriangle([
        FuzzyStatement("x", 2, "Средний", 0.0),
        FuzzyStatement("x", 5, "Средний", 1.0),
        FuzzyStatement("x", 8, "Средний", 0.0)
    ])
    
    high_x = FuzzyTriangle([
        FuzzyStatement("x", 5, "Высокий", 0.0),
        FuzzyStatement("x", 8, "Высокий", 1.0),
        FuzzyStatement("x", 10, "Высокий", 0.0)
    ])
    
    system = SugenoSystem()
    
    system.add_rule(
        conditions=[(low_x, 'x')],
        function=lambda inputs: 0.5 * inputs['x']
    )
    
    system.add_rule(
        conditions=[(medium_x, 'x')],
        function=lambda inputs: 2 * inputs['x']
    )
    
    system.add_rule(
        conditions=[(high_x, 'x')],
        function=lambda inputs: 3 * inputs['x']
    )
    
    return system


def make_approximation():
    system = create_approximation_system()

    print("=== Approximation ===")
    print()
    
    x_value = 0.4
    result = system.resolve({'x': x_value})
    print("Test with 1 x:")
    print(f"x = {x_value:.4f}: y = {result:.4f}")
    
    test_points = [0.1, 0.4, 1.0, 2.0, 2.9]
    print("\nTest with few xs:")
    for x in test_points:
        y = system.resolve({'x': x})
        print(f"  x={x:.4f}: y={y:.4f}")
    
def make_calculation():
    print("\n=== Calculation ===")
    
    temp_low = FuzzyTriangle([
        FuzzyStatement("Температура", 0, "низкая", 1.0),
        FuzzyStatement("Температура", 15, "низкая", 1.0),
        FuzzyStatement("Температура", 20, "низкая", 0.0)
    ])
    
    temp_high = FuzzyTriangle([
        FuzzyStatement("Температура", 15, "высокая", 0.0),
        FuzzyStatement("Температура", 25, "высокая", 1.0),
        FuzzyStatement("Температура", 30, "высокая", 1.0)
    ])
    
    humidity_low = FuzzyTriangle([
        FuzzyStatement("Влажность", 0, "низкая", 1.0),
        FuzzyStatement("Влажность", 30, "низкая", 1.0),
        FuzzyStatement("Влажность", 50, "низкая", 0.0)
    ])
    
    humidity_high = FuzzyTriangle([
        FuzzyStatement("Влажность", 40, "высокая", 0.0),
        FuzzyStatement("Влажность", 70, "высокая", 1.0),
        FuzzyStatement("Влажность", 100, "высокая", 1.0)
    ])
    
    system2 = SugenoSystem()
    
    # ЕСЛИ температура низкая И влажность низкая ТО мощность = 100
    system2.add_rule(
        conditions=[(temp_low, 'Температура'), (humidity_low, 'Влажность')],
        function=lambda inputs: 100
    )
    
    # ЕСЛИ температура высокая И влажность высокая ТО мощность = 20
    system2.add_rule(
        conditions=[(temp_high, 'Температура'), (humidity_high, 'Влажность')],
        function=lambda inputs: 20
    )
    
    # ЕСЛИ температура высокая ТО мощность = 40 - 0.5*влажность
    system2.add_rule(
        conditions=[(temp_high, 'Температура')],
        function=lambda inputs: 40 - 0.5 * inputs['Влажность']
    )
    
    test_cases = [
        ({'Температура': 10, 'Влажность': 20}, None),   # холодно и сухо
        ({'Температура': 28, 'Влажность': 80}, None),   # жарко и влажно
        ({'Температура': 20, 'Влажность': 60}, None)    # средние условия
    ]
    
    for inputs, _ in test_cases:
        power = system2.resolve(inputs)
        print(f"  Температура={inputs['Температура']}°C, Влажность={inputs['Влажность']}% -> Мощность={power:.2f}")

if __name__ == "__main__":
    make_approximation()
