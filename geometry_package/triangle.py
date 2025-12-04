from geometry_package.shape import Shape
from typing import Optional
import math


class Triangle(Shape):
    """Класс треугольника (по трём сторонам)"""

    def __init__(self, a: float, b: float, c: float):
        self._a = a
        self._b = b
        self._c = c
        self.validate()

    @property
    def sides(self) -> tuple:
        return (self._a, self._b, self._c)

    @property
    def area(self) -> float:
        if self._area is None:
            # Формула Герона
            s = (self._a + self._b + self._c) / 2
            self._area = math.sqrt(s * (s - self._a) * (s - self._b) * (s - self._c))
        return self._area

    @property
    def circumscribed_radius(self) -> float:
        if self._circumscribed_radius is None:
            # R = abc / 4S
            self._circumscribed_radius = (self._a * self._b * self._c) / (4 * self.area)
        return self._circumscribed_radius

    @property
    def inscribed_radius(self) -> float:
        if self._inscribed_radius is None:
            # r = 2S / (a + b + c)
            perimeter = self._a + self._b + self._c
            self._inscribed_radius = (2 * self.area) / perimeter
        return self._inscribed_radius

    def validate(self) -> bool:
        a, b, c = self.sides
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Все стороны должны быть положительными")

        # Проверка неравенства треугольника
        if not (a + b > c and a + c > b and b + c > a):
            raise ValueError("Треугольник с такими сторонами не существует")

        return True

    # Дополнительные dunder методы
    def __contains__(self, item):
        """Проверка, является ли треугольник прямоугольным"""
        a, b, c = sorted(self.sides)
        return math.isclose(c ** 2, a ** 2 + b ** 2, rel_tol=1e-9)

    def __getitem__(self, index):
        return self.sides[index]