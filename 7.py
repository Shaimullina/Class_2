"""Задача 7: Паттерн Observer с событийной системой
Реализуй паттерн Observer для создания событийной системы уведомлений.
Создай классы для различных типов событий (новости, акции, системные уведомления) и подписчиков (email, SMS, push-уведомления).
Используй абстрактные классы и множественное наследование для создания гибкой системы уведомлений
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging


class Observer(ABC):
    """
    Класс, который получает уведомления об изменениях
    """

    @abstractmethod
    def update(self, event: "Event") -> None:
        """
        Метод, который вызывается когда получает событие.
        """
        pass


class Subject(ABC):
    """
    Класс, к которому могут быть привязаны наблюдатели
    """

    def __init__(self) -> None:
        """
        Инциализирует список наблюдателей
        """
        self._observers = []

    def attach(self, observer) -> None:
        """
        Добавляет наблюдателей
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """
        Удаляет наблюжателя из подписчиков
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event):
        """
        Уведомляет всех наблюдателей о событии
        """
        for observer in self._observers:
            observer.update(event)


class Event(ABC):
    """
    Базовый класс для событий
    """

    def __init__(self, title: str, content: str) -> None:
        self.title = title
        self.content = content
        self.timestamp = datetime.now()


class NewsEvent(Event):
    """
    Класс события новостей
    """

    def __init__(self, title: str, content: str) -> None:
        super().__init__(title, content)


class PromoEvent(Event):
    """
    Класс с рекламной акцией
    """

    def __init__(self, title: str, content: str, expiry_date: datetime) -> None:
        super().__init__(title, content)
        self.expiry_date = expiry_date


class EmailNotifier(Observer):
    """
    Подписчик, который получает уведомления по эл. почте
    """

    def __init__(self, email: str) -> None:
        self.email = email

    def update(self, event: Event) -> None:
        print(f"[Email] To: {self.email} | New event: {event.title} - {event.content}")


class SMSNotifier(Observer):
    """
    Подписчик получает увед по СМС
    """

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def update(self, event: Event) -> None:
        print(
            f"[SMS] To: {self.phone_number} | New event: {event.title} - {event.content}"
        )


class PushNotifier(Observer):
    """
    Подписчик получает пуш увед
    """

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def update(self, event):
        print(
            f"[Push] To Device: {self.device_id} | New event: {event.title} - {event.content}"
        )


class NotificationCenter(Subject):
    """
    Все уведомления хранятся здесь
    """

    def publish_event(self, event: Event) -> None:
        print(f"\n[NotificationCenter] Publishing event: {event.title}")
        self.notify(event)


# Пример использования
notification_center = NotificationCenter()
email_notifier = EmailNotifier("user@example.com")
sms_notifier = SMSNotifier("+1234567890")

notification_center.attach(email_notifier)
notification_center.attach(sms_notifier)

news_event = NewsEvent("Важные новости", "Содержание новости")
promo_event = PromoEvent("Скидка 50%", "На все товары", datetime(2024, 12, 31))

notification_center.publish_event(news_event)
notification_center.publish_event(promo_event)
