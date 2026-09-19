from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send():
        pass

class EmailNotification(Notification):
    def send(self):
        print("Sending email")

class SmsNotification(Notification):
    def send(self):
        print("Sending sms")

class PushNotification(Notification):
    def send(self):
        print("Sending push")

# =================================================
class NotificationFactory(ABC):
    @abstractmethod
    def create(self):
        pass


class EmailFactory(NotificationFactory):
    def create(self):
        return EmailNotification()

class SmsFactory(NotificationFactory):
    def create(self):
        return SmsNotification()

class PushFactory(NotificationFactory):
    def create(self):
        return PushNotification()


def main():
    factory: NotificationFactory = SmsFactory()
    notification: Notification = factory.create();
    notification.send()

if __name__ == "__main__":
    main()