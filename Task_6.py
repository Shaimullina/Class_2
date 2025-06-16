"""
Задача 6: Декораторы классов и методов для логирования
Создай систему логирования для методов класса, используя декораторы.
Реализуй декоратор класса, который автоматически добавляет логирование ко всем
публичным методам, и декораторы методов для различных уровней логирования
(debug, info, warning, error).
Создай класс Calculator с различными математическими операциями
"""

import functools
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def log_method(level="info"):
    """
    Создается функция-декоратор, который принимает уровень логирования
    """

    def decorator(func):
        """
        Внутри декоратора определяется "wrapper", он облрачивает вызываемую функцию
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = None
            try:
                result = func(self, *args, **kwargs)
                msg = f"{timestamp} - {level.upper()}: Вызов {func.__name__} с args={args}, kwargs={kwargs} -> результат={result}"
            except Exception as e:
                msg = (
                    f"{timestamp} - {level.upper()}: Исключение в {func.__name__}: {e}"
                )
                logger.exception(msg)
                raise

            return result

        return wrapper

    return decorator


"""
декоратор "log_all_methods" перебирает атрибуты класса
"""


def log_all_methods(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("_"):
            decorated_method = log_method("info")(attr_value)
            setattr(cls, attr_name, decorated_method)
    return cls


@log_all_methods
class Calculator:
    def __init__(self):
        pass

    @log_method("debug")
    def add(self, a, b):
        return a + b

    @log_method("info")
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль")
        return a / b

    @log_method("warning")
    def power(self, base, exponent):
        return base**exponent


# Пример использования
calc = Calculator()
result1 = calc.add(5, 3)
result2 = calc.divide(10, 2)
result3 = calc.power(2, 10)
