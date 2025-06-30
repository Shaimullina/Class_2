"""Задача 7: Паттерн Observer с событийной системой
Реализуй паттерн Observer для создания событийной системы уведомлений.
Создай классы для различных типов событий (новости, акции, системные уведомления) и подписчиков (email, SMS, push-уведомления).
Используй абстрактные классы и множественное наследование для создания гибкой системы уведомлений
"""

from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
        self._observers = []

    def attach(self, observer) -> None:
        """
        Добавляет наблюдателей
        """
        if observer not in self._observers:
            self._observers.append(observer)
            logging.info(f"Attached observer: {observer.__class__.__name__}")

    def detach(self, observer: Observer) -> None:
        """
        Удаляет наблюжателя из подписчиков
        """
        if observer in self._observers:
            self._observers.remove(observer)
            logging.info(f"Detached observer: {observer.__class__.__name__}")

    def notify(self, event: "Event") -> None:
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
        """
        Обрабатывает событие и отправляет email-уведомление.
        """
        logging.info(f"[Email] To: {self.email} | {event.title} - {event.content}")


class SMSNotifier(Observer):
    """
    Подписчик получает увед по СМС
    """

    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def update(self, event: Event) -> None:
        """
        Обрабатывает событие и отправляет SMS сообщение.
        """
        logging.info(f"[SMS] To: {self.phone_number} | {event.title} - {event.content}")


class PushNotifier(Observer):
    """
    Подписчик получает пуш увед
    """

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id

    def update(self, event: Event) -> None:
        """
        Обрабатывает событие и отправляет push увед.
        """
        logging.info(
            f"[Push] To Device: {self.device_id} | {event.title} - {event.content}"
        )


class NotificationCenter(Subject):
    """
    Все уведомления хранятся здесь
    """

    def publish_event(self, event: Event) -> None:
        logging.info(f"[NotificationCenter] Publishing event: {event.title}")
        self.notify(event)


notification_center = NotificationCenter()
email_notifier = EmailNotifier("user@example.com")
sms_notifier = SMSNotifier("+1234567890")

notification_center.attach(email_notifier)
notification_center.attach(sms_notifier)

news_event = NewsEvent("Важные новости", "Содержание новости")
promo_event = PromoEvent("Скидка 50%", "На все товары", datetime(2024, 12, 31))

notification_center.publish_event(news_event)
notification_center.publish_event(promo_event)
