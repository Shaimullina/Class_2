"""Задача 6: Декораторы классов и методов для логирования
Создай систему логирования для методов класса, используя декораторы.
Реализуй декоратор класса, который автоматически добавляет логирование ко всем
публичным методам, и декораторы методов для различных уровней логирования
(debug, info, warning, error).
Создай класс Calculator с различными математическими операциями"""

import functools
from datetime import datetime
import logging
from typing import Callable, Any, Type

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_method(level: str = "info") -> Callable:
    def decorator(func: Callable) -> Callable:
        """
        Декоратор для вызова метода
        """

        @functools.wraps(func)
        def wrapper(self, *args: Any, **kwargs: Any) -> Any:
            result = None
            try:
                result = func(self, *args, **kwargs)
                message = f"Вызов {func.__name__} с args={args}, kwargs={kwargs} -> результат={result}"
                getattr(logging, level.lower())(message)
            except Exception as e:
                message = f"Исключение в {func.__name__}: {e}"
                logging.error(message)
                raise
            return result

        return wrapper

    return decorator


def log_all_methods(cls: Type) -> Type:
    """
    Декоратор, который добавляет ко всем публичным методам логирование
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and not attr_name.startswith("_"):
            decorated_method = log_method("info")(attr_value)
            setattr(cls, attr_name, decorated_method)
    return cls


@log_all_methods
class Calculator:
    """
    Калькулятор с методами для выполнения математических операций и логированием.
    """

    def __init__(self) -> None:
        pass

    @log_method("debug")
    def add(self, a: float, b: float) -> float:
        """
        Складывает два числа
        """
        return a + b

    @log_method("info")
    def divide(self, a: float, b: float) -> float:
        """
        Выполняет депление одно числа на другое
        """
        if b == 0:
            raise ValueError("Деление на ноль")
        return a / b

    @log_method("warning")
    def power(self, base: float, exponent: float) -> float:
        """
        Возводит число в степень
        """
        return base**exponent


# Пример использования
calc = Calculator()
result1 = calc.add(5, 3)
result2 = calc.divide(10, 2)
result3 = calc.power(2, 10)
