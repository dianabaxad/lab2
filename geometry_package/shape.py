from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class Shape(ABC):
    """Абстрактный базовый класс для геометрических фигур"""

    def __init_subclass__(cls, **kwargs):
        """Добавляем managed-атрибуты при создании подкласса"""
        super().__init_subclass__(**kwargs)
        cls._area = None
        cls._circumscribed_radius = None
        cls._inscribed_radius = None

    @property
    @abstractmethod
    def area(self) -> float:
        """Площадь фигуры"""
        pass

    @property
    @abstractmethod
    def circumscribed_radius(self) -> Optional[float]:
        """Радиус описанной окружности (если существует)"""
        pass

    @property
    @abstractmethod
    def inscribed_radius(self) -> Optional[float]:
        """Радиус вписанной окружности (если существует)"""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Проверка валидности фигуры"""
        pass

    # Dunder методы
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: площадь={self.area:.2f}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__dict__})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Shape):
            return False
        return math.isclose(self.area, other.area, rel_tol=1e-9)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area < other.area