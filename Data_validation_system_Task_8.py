"""Задача 8: Метаклассы и дескрипторы для валидации данных
Создай систему валидации данных, используя метаклассы и дескрипторы.
Реализуй дескрипторы для различных типов валидации (email, телефон, возраст) и
метакласс, который автоматически применяет валидацию к атрибутам класса на основе их аннотаций типов.
Создай класс User с различными полями, требующими валидации"""

import re
from typing import Any, Optional, Type, Callable, get_type_hints


class ValidatedDescriptor:
    """
    Валидация значений здесь происходит через заданный валидатор
    """

    def __init__(self, validator=None) -> None:
        self.validator = validator
        self.name = None

    def __set_name__(self, owner: Type, name: str) -> None:
        """
        Обозначает имя атрибута при создании класса
        """
        self.name = name

    def __get__(self, obj, objtype=None) -> Any:
        """
        Возвращает текущее значение атрибута
        """
        return obj.__dict__.get(self.name)

    def __set__(self, obj: Any, value: Any) -> None:
        """
        Устанавливает значение и валидирует его
        """
        if self.validator:
            if not self.validator(value):
                raise ValueError(f"Некорректное значение для '{self.name}': {value}")
        obj.__dict__[self.name] = value


class EmailValidator:
    """
    Валидатор эл. адресов
    """

    email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __call__(self, value: Any) -> bool:
        """
        Осуществление проверки email
        """
        return isinstance(value, str) and bool(self.email_regex.match(value))


class PhoneValidator:
    """
    Валидатор мобильных номеров
    """

    phone_regex = re.compile(r"^\+?\d[\d\-\s]{7,}\d$")

    def __call__(self, value: Any) -> bool:
        """
        Проверка номера телефона
        """
        return isinstance(value, str) and bool(self.phone_regex.match(value))


class AgeValidator:
    """
    Валидатор возраста
    """

    def __call__(self, value: Any) -> bool:
        """
        Проверка возраста
        """
        return isinstance(value, int) and (0 <= value <= 150)


def select_validator(attr_name: str, attr_type: type):
    """
    Возвращает соответствующий валидатор по имени и типу атрибута.
    """
    if attr_type == str:
        if "email" in attr_name.lower():
            return EmailValidator()
        if "phone" in attr_name.lower():
            return PhoneValidator()
    elif attr_type == int:
        return AgeValidator()
    return None


class ValidationMeta(type):
    """
    Метокласс, который назначает дискрипторы валидации на основе анотации
    """

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> Type:
        annotations = namespace.get("__annotations__", {})
        for attr_name, attr_type in annotations.items():
            validator = select_validator(attr_name, attr_type)
            namespace[attr_name] = ValidatedDescriptor(validator)
        return super().__new__(mcs, name, bases, namespace)


class User(metaclass=ValidationMeta):
    """
    Класс пользователя
    """

    email: str
    phone: str
    age: int

    def __init__(self, email: str, phone: str, age: int, name: str) -> None:
        self.email = email
        self.phone = phone
        self.age = age
        self.name = name

    def __str__(self) -> str:
        """
        возвращает строковое представление пользователя
        """

        return f"User({self.name}, {self.email}, {self.phone}, {self.age})"


# Пример использования
try:
    user1 = User("test@example.com", "+7-123-456-78-90", 25, "Иван")
    print(user1)
    user2 = User("invalid-email", "123", -5, "Петр")
except ValueError as e:
    print(f"Ошибка валидации: {e}")
