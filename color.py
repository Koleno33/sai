# Colors classification task (Mamdani)

from statements.fuzzyset import FuzzySet
from statements.statement import FuzzyStatement
from statements.fuzzyset import FuzzyTriangle
from typing import List

class Color:
    def __init__(self, R: int, G: int, B: int):
        self.R = R
        self.G = G
        self.B = B

    def __str__(self):
        return f"{self.R} {self.G} {self.B}"


class ColorRule:
    def __init__(self, name, R: FuzzyTriangle, G: FuzzyTriangle, B: FuzzyTriangle):
        self.name = name
        self.R = R
        self.G = G
        self.B = B


class ColorPicker:
    def __init__(self, R: List['FuzzyTriangle'], G: List['FuzzyTriangle'], B: List['FuzzyTriangle']):
        self.R = R
        self.G = G
        self.B = B

    def resolve(self, color: Color, rule: ColorRule):
        found_triangle_R = None
        for red_triangle in self.R:
            if red_triangle is rule.R:
                found_triangle_R = red_triangle
        assert(found_triangle_R is not None)

        found_triangle_G = None
        for green_triangle in self.G:
            if green_triangle is rule.G:
                found_triangle_G = green_triangle
        assert(found_triangle_G is not None)

        found_triangle_B = None
        for blue_triangle in self.B:
            if blue_triangle is rule.B:
                found_triangle_B = blue_triangle
        assert(found_triangle_B is not None)

        red_validity = found_triangle_R.resolve(color.R)
        green_validity = found_triangle_G.resolve(color.G)
        blue_validity = found_triangle_B.resolve(color.B)

        print(red_validity, green_validity, blue_validity)
        return min(red_validity, green_validity, blue_validity)


def main():
    light_pink = Color(219, 143, 178)
    light_pink_R =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с красной компонентой", 240, "светло розовый", 1.0), 
                          FuzzyStatement("цвет с красной компонентой", 180, "светло розовый", 0.0), 
                          FuzzyStatement("цвет с красной компонентой", 255, "светло розовый", 1.0), ]
                    )
    light_pink_G =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с зеленой компонентой", 127, "светло розовый", 1.0), 
                          FuzzyStatement("цвет с зеленой компонентой", 100, "светло розовый", 0.0), 
                          FuzzyStatement("цвет с зеленой компонентой", 180, "светло розовый", 0.0), ]
                    )
    light_pink_B =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с синей компонентой", 127, "светло розовый", 1.0), 
                          FuzzyStatement("цвет с синей компонентой", 100, "светло розовый", 0.0), 
                          FuzzyStatement("цвет с синей компонентой", 180, "светло розовый", 0.0), ]
                    )
    light_pink_rule = ColorRule(light_pink, light_pink_R, light_pink_G, light_pink_B)

    mint = Color(111, 227, 144)
    mint_R =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с красной компонентой", 112, "мятный", 1.0), 
                          FuzzyStatement("цвет с красной компонентой", 130, "мятный", 0.0), 
                          FuzzyStatement("цвет с красной компонентой", 80,  "мятный", 0.0), ]
                    )
    mint_G =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с зеленой компонентой", 212, "мятный", 1.0), 
                          FuzzyStatement("цвет с зеленой компонентой", 240, "мятный", 0.0), 
                          FuzzyStatement("цвет с зеленой компонентой", 200, "мятный", 1.0), ]
                    )
    mint_B =  FuzzyTriangle(
                        [ FuzzyStatement("цвет с синей компонентой", 162, "мятный", 1.0), 
                          FuzzyStatement("цвет с синей компонентой", 190, "мятный", 0.0), 
                          FuzzyStatement("цвет с синей компонентой", 140, "мятный", 0.0), ]
                    )
    mint_rule = ColorRule(light_pink, light_pink_R, light_pink_G, light_pink_B)
    
    cp = ColorPicker(
        [
            light_pink_R,
            mint_R,
        ],
        [
            light_pink_G,
            mint_G,
        ],
        [
            light_pink_B,
            mint_B,
        ]
    )

    rule_validity = cp.resolve(light_pink, light_pink_rule)
    print(f"Цвет {light_pink} светло розовый с истинностью {rule_validity}")


if __name__ == "__main__":
    main()

