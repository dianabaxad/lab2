import sqlite3
from typing import List, Tuple, Optional
import os

class DatabaseManager:
    """Менеджер для работы с существующей базой данных SQLite"""

    class DatabaseManager:
        def __init__(self, db_name: str = None):
            # Берём путь из ENV, иначе используем стандартный
            self.db_name = db_name or os.getenv("DB_PATH", "geometry_calculations.db")
            self._validate_database()

    def _validate_database(self):
        """Проверка существования и структуры базы данных"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Проверяем существование таблицы calculations
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='calculations'
                """)
                if not cursor.fetchone():
                    raise ValueError(
                        f"Таблица 'calculations' не найдена в базе данных {self.db_name}. "
                        "Убедитесь, что база данных правильно инициализирована."
                    )
        except sqlite3.Error as e:
            raise ConnectionError(
                f"Ошибка подключения к базе данных {self.db_name}: {e}"
            )

    def save_calculation(self, shape_type: str, parameters: str,
                         area: float, circumscribed_radius: Optional[float],
                         inscribed_radius: Optional[float]) -> int:
        """Сохранение расчета в базу данных"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO calculations 
                (shape_type, parameters, area, circumscribed_radius, inscribed_radius)
                VALUES (?, ?, ?, ?, ?)
            ''', (shape_type, parameters, area, circumscribed_radius, inscribed_radius))
            conn.commit()
            return cursor.lastrowid

    def get_all_calculations(self, limit: int = 100) -> List[Tuple]:
        """Получение всех расчетов с ограничением по количеству"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, shape_type, parameters, area, 
                       circumscribed_radius, inscribed_radius, 
                       datetime(timestamp, 'localtime')
                FROM calculations 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def get_calculations_by_shape(self, shape_type: str, limit: int = 50) -> List[Tuple]:
        """Получение расчетов по типу фигуры"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM calculations 
                WHERE shape_type = ? 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (shape_type, limit))
            return cursor.fetchall()

    def get_statistics(self) -> dict:
        """Получение статистики по расчетам"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM calculations')
            total = cursor.fetchone()[0]

            cursor.execute('''
                SELECT shape_type, COUNT(*) as count, 
                       AVG(area) as avg_area,
                       MIN(area) as min_area,
                       MAX(area) as max_area
                FROM calculations 
                GROUP BY shape_type
            ''')

            by_shape = cursor.fetchall()

            # Дополнительная статистика
            cursor.execute('SELECT MAX(timestamp) FROM calculations')
            last_calculation = cursor.fetchone()[0]

            return {
                'total': total,
                'by_shape': by_shape,
                'last_calculation': last_calculation
            }

    def clear_history(self, confirm: bool = False) -> int:
        """
        Очистка истории расчетов.
        Требует явного подтверждения.
        """
        if not confirm:
            return 0

        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM calculations')
            count = cursor.fetchone()[0]

            cursor.execute('DELETE FROM calculations')
            conn.commit()

            return count

    def get_recent_calculations(self, count: int = 5) -> List[Tuple]:
        """Получение последних расчетов"""
        return self.get_all_calculations(limit=count)