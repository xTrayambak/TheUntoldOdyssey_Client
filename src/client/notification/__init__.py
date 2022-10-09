from enum import Enum

class NotificationType(Enum):
    POPUP = 0
    TOAST = 1

class Notification:
    def __init__(self, tuo, header: str, description: str, notif_type: NotificationType):
        self.tuo = tuo
        self.header = header
        self.description = description
        self.notif_type = notif_type


    def play_out(self):
        notif_audio = self.tuo.audio_loader.load('assets/sounds/notification.wav')
        notif_audio.play()

        if self.notif_type == NotificationType.POPUP:
            self.tuo.warn(self.header, self.description)
