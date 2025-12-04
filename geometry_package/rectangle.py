from geometry_package.shape import Shape
from typing import Optional
import math

class Rectangle(Shape):
    """Класс прямоугольника"""

    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height
        self.validate()

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = value
        self._area = None
        self._circumscribed_radius = None

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = value
        self._area = None
        self._circumscribed_radius = None

    @property
    def area(self) -> float:
        if self._area is None:
            self._area = self.width * self.height
        return self._area

    @property
    def circumscribed_radius(self) -> float:
        if self._circumscribed_radius is None:
            # Диагональ прямоугольника / 2
            diagonal = math.sqrt(self.width ** 2 + self.height ** 2)
            self._circumscribed_radius = diagonal / 2
        return self._circumscribed_radius

    @property
    def inscribed_radius(self) -> Optional[float]:
        # Вписанная окружность существует только для квадрата
        if math.isclose(self.width, self.height, rel_tol=1e-9):
            return min(self.width, self.height) / 2
        return None

    def validate(self) -> bool:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Ширина и высота должны быть положительными")
        return True

    # Дополнительные dunder методы
    def __add__(self, other):
        if isinstance(other, Rectangle):
            return Rectangle(self.width + other.width, self.height + other.height)
        return NotImplemented

    def __mul__(self, scalar):
        if isinstance(scalar, (int, float)):
            return Rectangle(self.width * scalar, self.height * scalar)
        return NotImplemented