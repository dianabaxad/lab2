from geometry_package.shape import Shape
from typing import Optional
import math

class Trapezoid(Shape):
    """Класс трапеции (равнобедренной)"""

    def __init__(self, base1: float, base2: float, height: float):
        self._base1 = base1
        self._base2 = base2
        self._height = height
        self.validate()

    @property
    def bases(self) -> tuple:
        return (self._base1, self._base2)

    @property
    def height(self) -> float:
        return self._height

    @property
    def area(self) -> float:
        if self._area is None:
            self._area = (self._base1 + self._base2) * self._height / 2
        return self._area

    @property
    def side_length(self) -> float:
        """Длина боковой стороны (для равнобедренной трапеции)"""
        base_diff = abs(self._base1 - self._base2) / 2
        return math.sqrt(base_diff ** 2 + self._height ** 2)

    @property
    def circumscribed_radius(self) -> Optional[float]:
        # Описанная окружность существует только если трапеция равнобедренная
        # и суммы противоположных углов равны 180 градусам
        # Для упрощения считаем, что всегда существует для равнобедренной
        if self._circumscribed_radius is None:
            # Используем формулу через стороны и диагонали
            a, b = sorted([self._base1, self._base2])
            c = self.side_length
            diagonal = math.sqrt(a * b + c ** 2)
            self._circumscribed_radius = (c * diagonal) / (2 * self._height)
        return self._circumscribed_radius

    @property
    def inscribed_radius(self) -> Optional[float]:
        # Вписанная окружность существует если суммы противоположных сторон равны
        if math.isclose(self._base1 + self._base2, 2 * self.side_length, rel_tol=1e-9):
            return self._height / 2
        return None

    def validate(self) -> bool:
        if self._base1 <= 0 or self._base2 <= 0 or self._height <= 0:
            raise ValueError("Все параметры должны быть положительными")
        return True

    # Дополнительные dunder методы
    def __len__(self):
        """Возвращает количество сторон"""
        return 4

    def __iter__(self):
        """Итерация по сторонам трапеции"""
        yield self._base1
        yield self._base2
        yield self.side_length
        yield self.side_length