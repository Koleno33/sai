from sugeno import SugenoSystem, Rule
from statements.fuzzyset import FuzzyTriangle
from statements.statement import FuzzyStatement
import math
import matplotlib.pyplot as plt
import numpy as np

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

    low_y = FuzzyTriangle([
        FuzzyStatement("y", 0, "Низкий", 0.0),
        FuzzyStatement("y", 2, "Низкий", 1.0),
        FuzzyStatement("y", 5, "Низкий", 0.0)
    ])
    
    medium_y = FuzzyTriangle([
        FuzzyStatement("y", 2, "Средний", 0.0),
        FuzzyStatement("y", 5, "Средний", 1.0),
        FuzzyStatement("y", 8, "Средний", 0.0)
    ])
    
    high_y = FuzzyTriangle([
        FuzzyStatement("y", 5, "Высокий", 0.0),
        FuzzyStatement("y", 8, "Высокий", 1.0),
        FuzzyStatement("y", 10, "Высокий", 0.0)
    ])
    
    system = SugenoSystem()
    
    system.add_rule(
        conditions=[(low_x, 'x'), (low_y, 'y')],
        function=lambda inputs: 0.5 * inputs['x'] + 0.7 * inputs['y'] + 0.5
    )
    
    system.add_rule(
        conditions=[(low_x, 'x'), (medium_y, 'y')],
        function=lambda inputs: 0.45 * inputs['x'] + 0.8 * inputs['y'] + 0.25
    )
    
    system.add_rule(
        conditions=[(low_x, 'x'), (high_y, 'y')],
        function=lambda inputs: 0.6 * inputs['x'] + 0.2 * inputs['y'] - 0.3
    )

    system.add_rule(
        conditions=[(medium_x, 'x'), (low_y, 'y')],
        function=lambda inputs: 1.5*inputs['x'] + 0.5*inputs['y'] - 1.0
    )
    
    system.add_rule(
        conditions=[(medium_x, 'x'), (medium_y, 'y')],
        function=lambda inputs: 2.0*inputs['x'] + 0.8*inputs['y'] - 2.5
    )
    
    system.add_rule(
        conditions=[(medium_x, 'x'), (high_y, 'y')],
        function=lambda inputs: 1.8*inputs['x'] + 0.6*inputs['y'] - 3.0
    )
    
    system.add_rule(
        conditions=[(high_x, 'x'), (low_y, 'y')],
        function=lambda inputs: 2.5*inputs['x'] + 0.7*inputs['y'] - 4.0
    )
    
    system.add_rule(
        conditions=[(high_x, 'x'), (medium_y, 'y')],
        function=lambda inputs: 3.0*inputs['x'] + 0.9*inputs['y'] - 6.0
    )
    
    system.add_rule(
        conditions=[(high_x, 'x'), (high_y, 'y')],
        function=lambda inputs: 2.8*inputs['x'] + 0.8*inputs['y'] - 7.0
    )
    
    return system

def test_approximation():
    def target_func(x, y):
        return x**2 * math.sin(x) + math.sqrt(y) * math.cos(y)
    
    system = create_approximation_system()
    
    test_points = [
        (0.5, 1.0), (1.0, 2.0), (1.5, 3.0),
        (2.0, 4.0), (2.5, 5.0), (3.0, 6.0),
        (3.5, 7.0), (4.0, 8.0), (4.5, 9.0)
    ]
    
    print("===============================")
    print("\nTest points:\n")
    print(f"{'x':^8} | {'y':^8} | {'Истинное z':^12} | {'Сугено':^12} | {'Ошибка':^10} |")
    print("-------------------------------")
    
    total_error = 0
    
    for x, y in test_points:
        true_z = target_func(x, y)
        
        res = system.resolve({'x': x, 'y': y})
        
        error = abs(true_z - res)
        
        total_error += error
        
        print(f"{x:^8.2f} | {y:^8.2f} | {true_z:^12.4f} | {res:^12.4f} | {error:^10.4f} |")
    
    print("--------------------------------")
    print(f"\nAverage error:")
    print(f"  Sugeno: {total_error/len(test_points):.4f}")

def visualize_approximation():
    system = create_approximation_system()
    
    x_vals = np.linspace(0, 10, 100)
    y_vals = np.linspace(0, 10, 100)
    X, Y = np.meshgrid(x_vals, y_vals)
    
    Z_true = np.zeros_like(X)
    Z_sugeno = np.zeros_like(X)
    
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            x_val = X[i, j]
            y_val = Y[i, j]
            
            Z_true[i, j] = x_val**2 * math.sin(x_val) + math.sqrt(y_val) * math.cos(y_val)
            
            Z_sugeno[i, j] = system.resolve({'x': x_val, 'y': y_val})
    
    Z_error = np.abs(Z_true - Z_sugeno)
    
    plt.figure(figsize=(15, 4))
    
    t_points = np.linspace(0, 10, 200)
    
    z_true_xy = np.array([t**2 * math.sin(t) + math.sqrt(t) * math.cos(t) for t in t_points])
    z_sugeno_xy = np.array([system.resolve({'x': t, 'y': t}) for t in t_points])
    z_error_xy = np.abs(z_true_xy - z_sugeno_xy)
    
    plt.subplot(1, 4, 1)
    plt.contourf(X, Y, Z_true, levels=30, cmap='viridis', alpha=0.7)
    plt.plot(t_points, t_points, 'r-', linewidth=3, label='Срез: x = y')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('XY: Срез (диагональ x=y)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 4, 2)
    plt.plot(t_points, z_true_xy, 'b-', linewidth=2)
    plt.xlabel('x = y')
    plt.ylabel('z')
    plt.title('XY: Истинная функция\nвдоль диагонали')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 4, 3)
    plt.plot(t_points, z_sugeno_xy, 'r-', linewidth=2)
    plt.xlabel('x = y')
    plt.ylabel('z')
    plt.title('XY: Аппроксимация Сугено\nвдоль диагонали')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 4, 4)
    plt.plot(t_points, z_error_xy, 'g-', linewidth=2)
    plt.xlabel('x = y')
    plt.ylabel('Ошибка')
    plt.title('XY: Абсолютная ошибка\nвдоль диагонали')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    plt.figure(figsize=(15, 4))
    
    y_fixed = 5.0
    x_points = np.linspace(0, 10, 200)
    
    z_true_xz = np.array([x**2 * math.sin(x) + math.sqrt(y_fixed) * math.cos(y_fixed) for x in x_points])
    
    z_sugeno_xz = np.array([system.resolve({'x': x, 'y': y_fixed}) for x in x_points])
    
    z_error_xz = np.abs(z_true_xz - z_sugeno_xz)
    
    # График 1: Срез y=5 на тепловой карте
    plt.subplot(1, 4, 1)
    plt.contourf(X, Y, Z_true, levels=30, cmap='viridis', alpha=0.7)
    plt.axhline(y=y_fixed, color='r', linewidth=3, label=f'Срез: y={y_fixed}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'XZ: Срез при y={y_fixed}')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # График 2: Истинная функция
    plt.subplot(1, 4, 2)
    plt.plot(x_points, z_true_xz, 'b-', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title(f'XZ: Истинная функция\n(y={y_fixed})')
    plt.grid(True, alpha=0.3)
    
    # График 3: Аппроксимация Сугено
    plt.subplot(1, 4, 3)
    plt.plot(x_points, z_sugeno_xz, 'r-', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('z')
    plt.title(f'XZ: Аппроксимация Сугено\n(y={y_fixed})')
    plt.grid(True, alpha=0.3)
    
    # График 4: Ошибка
    plt.subplot(1, 4, 4)
    plt.plot(x_points, z_error_xz, 'g-', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('Ошибка')
    plt.title(f'XZ: Абсолютная ошибка\n(y={y_fixed})')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 3. YZ проекция (x фиксировано = 5)
    plt.figure(figsize=(15, 4))
    
    x_fixed = 5.0
    y_points = np.linspace(0, 10, 200)
    
    # Истинные значения
    z_true_yz = np.array([x_fixed**2 * math.sin(x_fixed) + math.sqrt(y) * math.cos(y) for y in y_points])
    
    # Предсказания Сугено
    z_sugeno_yz = np.array([system.resolve({'x': x_fixed, 'y': y}) for y in y_points])
    
    # Ошибка
    z_error_yz = np.abs(z_true_yz - z_sugeno_yz)
    
    # График 1: Срез x=5 на тепловой карте
    plt.subplot(1, 4, 1)
    plt.contourf(X, Y, Z_true, levels=30, cmap='viridis', alpha=0.7)
    plt.axvline(x=x_fixed, color='r', linewidth=3, label=f'Срез: x={x_fixed}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'YZ: Срез при x={x_fixed}')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # График 2: Истинная функция
    plt.subplot(1, 4, 2)
    plt.plot(y_points, z_true_yz, 'b-', linewidth=2)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title(f'YZ: Истинная функция\n(x={x_fixed})')
    plt.grid(True, alpha=0.3)
    
    # График 3: Аппроксимация Сугено
    plt.subplot(1, 4, 3)
    plt.plot(y_points, z_sugeno_yz, 'r-', linewidth=2)
    plt.xlabel('y')
    plt.ylabel('z')
    plt.title(f'YZ: Аппроксимация Сугено\n(x={x_fixed})')
    plt.grid(True, alpha=0.3)
    
    # График 4: Ошибка
    plt.subplot(1, 4, 4)
    plt.plot(y_points, z_error_yz, 'g-', linewidth=2)
    plt.xlabel('y')
    plt.ylabel('Ошибка')
    plt.title(f'YZ: Абсолютная ошибка\n(x={x_fixed})')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 4. Функции принадлежности
    plt.figure(figsize=(12, 4))
    
    # Для x
    plt.subplot(1, 2, 1)
    x_points_mf = np.linspace(0, 10, 200)
    
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
    
    mu_low = [low_x.resolve(x) for x in x_points_mf]
    mu_medium = [medium_x.resolve(x) for x in x_points_mf]
    mu_high = [high_x.resolve(x) for x in x_points_mf]
    
    plt.plot(x_points_mf, mu_low, 'b-', linewidth=2, label='Низкий')
    plt.plot(x_points_mf, mu_medium, 'g-', linewidth=2, label='Средний')
    plt.plot(x_points_mf, mu_high, 'r-', linewidth=2, label='Высокий')
    plt.xlabel('x')
    plt.ylabel('Степень принадлежности')
    plt.title('Функции принадлежности для x')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Для y
    plt.subplot(1, 2, 2)
    y_points_mf = np.linspace(0, 10, 200)
    
    low_y = FuzzyTriangle([
        FuzzyStatement("y", 0, "Низкий", 0.0),
        FuzzyStatement("y", 2, "Низкий", 1.0),
        FuzzyStatement("y", 5, "Низкий", 0.0)
    ])
    
    medium_y = FuzzyTriangle([
        FuzzyStatement("y", 2, "Средний", 0.0),
        FuzzyStatement("y", 5, "Средний", 1.0),
        FuzzyStatement("y", 8, "Средний", 0.0)
    ])
    
    high_y = FuzzyTriangle([
        FuzzyStatement("y", 5, "Высокий", 0.0),
        FuzzyStatement("y", 8, "Высокий", 1.0),
        FuzzyStatement("y", 10, "Высокий", 0.0)
    ])
    
    mu_low_y = [low_y.resolve(y) for y in y_points_mf]
    mu_medium_y = [medium_y.resolve(y) for y in y_points_mf]
    mu_high_y = [high_y.resolve(y) for y in y_points_mf]
    
    plt.plot(y_points_mf, mu_low_y, 'b-', linewidth=2, label='Низкий')
    plt.plot(y_points_mf, mu_medium_y, 'g-', linewidth=2, label='Средний')
    plt.plot(y_points_mf, mu_high_y, 'r-', linewidth=2, label='Высокий')
    plt.xlabel('y')
    plt.ylabel('Степень принадлежности')
    plt.title('Функции принадлежности для y')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 5. Дополнительный график: сравнение в одной точке
    plt.figure(figsize=(12, 4))
    
    # Точка для анализа
    x_test, y_test = 3.0, 4.0
    
    # Вычисляем принадлежности для этой точки
    plt.subplot(1, 3, 1)
    
    # Создаем треугольники для x
    mu_x_low = low_x.resolve(x_test)
    mu_x_medium = medium_x.resolve(x_test)
    mu_x_high = high_x.resolve(x_test)
    
    plt.bar(['Низкий', 'Средний', 'Высокий'], [mu_x_low, mu_x_medium, mu_x_high], 
            color=['blue', 'green', 'red'])
    plt.xlabel('Термы для x')
    plt.ylabel('Степень принадлежности')
    plt.title(f'Принадлежности x={x_test}')
    plt.grid(True, alpha=0.3)
    
    # Принадлежности для y
    plt.subplot(1, 3, 2)
    mu_y_low = low_y.resolve(y_test)
    mu_y_medium = medium_y.resolve(y_test)
    mu_y_high = high_y.resolve(y_test)
    
    plt.bar(['Низкий', 'Средний', 'Высокий'], [mu_y_low, mu_y_medium, mu_y_high],
            color=['blue', 'green', 'red'])
    plt.xlabel('Термы для y')
    plt.ylabel('Степень принадлежности')
    plt.title(f'Принадлежности y={y_test}')
    plt.grid(True, alpha=0.3)
    
    # Сравнение истинного и предсказанного значения
    plt.subplot(1, 3, 3)
    true_z = x_test**2 * math.sin(x_test) + math.sqrt(y_test) * math.cos(y_test)
    pred_z = system.resolve({'x': x_test, 'y': y_test})
    
    plt.bar(['Истинное', 'Сугено'], [true_z, pred_z], color=['blue', 'orange'])
    plt.ylabel('z')
    plt.title(f'Сравнение для (x={x_test}, y={y_test})')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\nПример для точки (x={x_test}, y={y_test}):")
    print(f"  Истинное значение: {true_z:.4f}")
    print(f"  Предсказание Сугено: {pred_z:.4f}")
    print(f"  Абсолютная ошибка: {abs(true_z - pred_z):.4f}")

def main():
    test_approximation()
    visualize_approximation()


if __name__ == "__main__":
    main()
    

def main():
    test_approximation()
    visualize_approximation()


if __name__ == "__main__":
    main()

