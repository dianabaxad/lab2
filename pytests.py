import pytest
import math
from geometry_package.rectangle import Rectangle
from geometry_package.triangle import Triangle
from geometry_package.trapezoid import Trapezoid


class TestRectangle:
    """Тесты для класса Rectangle"""

    def test_rectangle_creation(self):
        """Тест создания прямоугольника"""
        rect = Rectangle(3, 4)
        assert rect.width == 3
        assert rect.height == 4

    def test_rectangle_area(self):
        """Тест вычисления площади"""
        rect = Rectangle(3, 4)
        assert rect.area == 12

    def test_square_area(self):
        """Тест площади квадрата"""
        square = Rectangle(5, 5)
        assert square.area == 25

    def test_rectangle_circumscribed_radius(self):
        """Тест радиуса описанной окружности"""
        rect = Rectangle(3, 4)
        expected = math.sqrt(3 ** 2 + 4 ** 2) / 2
        assert math.isclose(rect.circumscribed_radius, expected, rel_tol=1e-9)

    def test_inscribed_radius_square(self):
        """Тест вписанной окружности для квадрата"""
        square = Rectangle(4, 4)
        assert square.inscribed_radius == 2

    def test_inscribed_radius_rectangle(self):
        """Тест вписанной окружности для не-квадрата"""
        rect = Rectangle(3, 4)
        assert rect.inscribed_radius is None

    def test_rectangle_validation_positive(self):
        """Тест валидации положительных значений"""
        rect = Rectangle(5, 5)
        assert rect.validate() is True

    def test_rectangle_validation_negative(self):
        """Тест валидации отрицательных значений"""
        with pytest.raises(ValueError, match="положительными"):
            Rectangle(-1, 5)

    def test_rectangle_dunder_str(self):
        """Тест строкового представления"""
        rect = Rectangle(3, 4)
        assert "Rectangle" in str(rect)
        assert "12.00" in str(rect)

    def test_rectangle_equality(self):
        """Тест сравнения прямоугольников"""
        rect1 = Rectangle(3, 4)
        rect2 = Rectangle(3, 4)
        rect3 = Rectangle(6, 8)

        assert rect1 == rect2
        assert rect1 != rect3
        assert rect1 < rect3


class TestTriangle:
    """Тесты для класса Triangle"""

    def test_triangle_creation(self):
        """Тест создания треугольника"""
        tri = Triangle(3, 4, 5)
        assert tri.sides == (3, 4, 5)

    def test_right_triangle_area(self):
        """Тест площади прямоугольного треугольника"""
        tri = Triangle(3, 4, 5)
        assert tri.area == 6

    def test_equilateral_triangle_area(self):
        """Тест площади равностороннего треугольника"""
        tri = Triangle(5, 5, 5)
        expected = (math.sqrt(3) / 4) * 5 ** 2
        assert math.isclose(tri.area, expected, rel_tol=1e-9)

    def test_triangle_circumscribed_radius(self):
        """Тест радиуса описанной окружности"""
        tri = Triangle(3, 4, 5)
        assert tri.circumscribed_radius == 2.5

    def test_triangle_inscribed_radius(self):
        """Тест радиуса вписанной окружности"""
        tri = Triangle(3, 4, 5)
        assert tri.inscribed_radius == 1.0

    def test_triangle_validation_positive(self):
        """Тест валидации положительных сторон"""
        tri = Triangle(3, 4, 5)
        assert tri.validate() is True

    def test_triangle_validation_inequality(self):
        """Тест неравенства треугольника"""
        with pytest.raises(ValueError, match="не существует"):
            Triangle(1, 1, 3)

    def test_right_triangle_detection(self):
        """Тест определения прямоугольного треугольника"""
        right_tri = Triangle(3, 4, 5)
        non_right_tri = Triangle(5, 5, 5)

        assert right_tri in right_tri  # Это прямоугольный треугольник
        assert non_right_tri not in non_right_tri  # Это не прямоугольный

    def test_triangle_indexing(self):
        """Тест индексации сторон"""
        tri = Triangle(3, 4, 5)
        assert tri[0] == 3
        assert tri[1] == 4
        assert tri[2] == 5


class TestTrapezoid:
    """Тесты для класса Trapezoid"""

    def test_trapezoid_creation(self):
        """Тест создания трапеции"""
        trap = Trapezoid(5, 7, 4)
        assert trap.bases == (5, 7)
        assert trap.height == 4

    def test_trapezoid_area(self):
        """Тест площади трапеции"""
        trap = Trapezoid(5, 7, 4)
        expected = (5 + 7) * 4 / 2
        assert trap.area == expected

    def test_trapezoid_side_length(self):
        """Тест длины боковой стороны"""
        trap = Trapezoid(5, 7, 4)
        expected = math.sqrt(((7 - 5) / 2) ** 2 + 4 ** 2)
        assert math.isclose(trap.side_length, expected, rel_tol=1e-9)

    def test_trapezoid_perimeter(self):
        """Тест вычисления периметра через dunder методы"""
        trap = Trapezoid(5, 7, 4)
        sides = list(trap)
        assert len(sides) == 4
        assert sides[0] == 5  # base1
        assert sides[1] == 7  # base2

    def test_trapezoid_validation(self):
        """Тест валидации параметров"""
        trap = Trapezoid(5, 7, 4)
        assert trap.validate() is True

        with pytest.raises(ValueError):
            Trapezoid(0, 5, 4)

    def test_trapezoid_dunder_len(self):
        """Тест количества сторон"""
        trap = Trapezoid(5, 7, 4)
        assert len(trap) == 4
