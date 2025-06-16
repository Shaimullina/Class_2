"""
Задача 7: Паттерн Observer с событийной системой
Реализуй паттерн Observer для создания событийной системы уведомлений.
Создай классы для различных типов событий (новости, акции, системные уведомления) и подписчиков (email, SMS, push-уведомления).
Используй абстрактные классы и множественное наследование для создания гибкой системы уведомлений
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass


class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)


class Event(ABC):
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.timestamp = datetime.now()


class NewsEvent(Event):
    def __init__(self, title, content):
        super().__init__(title, content)


class PromoEvent(Event):
    def __init__(self, title, content, expiry_date):
        super().__init__(title, content)
        self.expiry_date = expiry_date


class EmailNotifier(Observer):
    def __init__(self, email):
        self.email = email

    def update(self, event):
        print(f"[Email] To: {self.email} | New event: {event.title} - {event.content}")


class SMSNotifier(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def update(self, event):
        print(
            f"[SMS] To: {self.phone_number} | New event: {event.title} - {event.content}"
        )


class PushNotifier(Observer):
    def __init__(self, device_id):
        self.device_id = device_id

    def update(self, event):
        print(
            f"[Push] To Device: {self.device_id} | New event: {event.title} - {event.content}"
        )


class NotificationCenter(Subject):
    def publish_event(self, event):
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
