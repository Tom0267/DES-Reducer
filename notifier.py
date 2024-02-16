from notifypy import Notify

class notif:
    def notify(self, title, message, urgency) -> None:
        
        self.notification.title = title
        self.notification.message = message
        self.notification.urgency = urgency
        self.notification.send()

    def __init__(self) -> None:
        self.notification = Notify(default_application_name="Eye Health", default_notification_limit=1)
        self.notification.title = "Eye Health"
        self.notification.icon = "Resources/Icon_small.ico"