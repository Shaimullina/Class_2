"""Задача 8: Метаклассы и дескрипторы для валидации данных
Создай систему валидации данных, используя метаклассы и дескрипторы.
Реализуй дескрипторы для различных типов валидации (email, телефон, возраст) и
метакласс, который автоматически применяет валидацию к атрибутам класса на основе их аннотаций типов.
Создай класс User с различными полями, требующими валидации"""

import re
from typing import get_type_hints


class ValidatedDescriptor:
    def __init__(self, validator=None):
        self.validator = validator
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if self.validator:
            if not self.validator(value):
                raise ValueError(f"Некорректное значение для '{self.name}': {value}")
        obj.__dict__[self.name] = value


class EmailValidator:
    email_regex = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

    def __call__(self, value):
        return isinstance(value, str) and bool(self.email_regex.match(value))


class PhoneValidator:
    phone_regex = re.compile(r"^\+?\d[\d\-\s]{7,}\d$")

    def __call__(self, value):
        return isinstance(value, str) and bool(self.phone_regex.match(value))


class AgeValidator:
    def __call__(self, value):
        return isinstance(value, int) and (0 <= value <= 150)


class ValidationMeta(type):
    def __new__(mcs, name, bases, namespace):
        annotations = namespace.get("__annotations__", {})
        for attr_name, attr_type in annotations.items():
            # В зависимости от типа, назначаем соответствующий дескриптор
            if attr_type == str:
                if "email" in attr_name.lower():
                    validator = EmailValidator()
                elif "phone" in attr_name.lower():
                    validator = PhoneValidator()
                else:
                    validator = None  # для обычных строк без проверки
            elif attr_type == int:
                validator = AgeValidator()
            else:
                validator = None
            namespace[attr_name] = ValidatedDescriptor(validator)
        return super().__new__(mcs, name, bases, namespace)


class User(metaclass=ValidationMeta):
    email: str  # будет автоматически валидироваться как email
    phone: str  # будет автоматически валидироваться как телефон
    age: int  # будет автоматически валидироваться как возраст

    def __init__(self, email, phone, age, name):
        self.email = email
        self.phone = phone
        self.age = age
        self.name = name

    def __str__(self):
        return f"User({self.name}, {self.email}, {self.phone}, {self.age})"


# Пример использования
try:
    user1 = User("test@example.com", "+7-123-456-78-90", 25, "Иван")
    print(user1)

    # Попытка создать пользователя с невалидными данными
    user2 = User("invalid-email", "123", -5, "Петр")
except ValueError as e:
    print(f"Ошибка валидации: {e}")
