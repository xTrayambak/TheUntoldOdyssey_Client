from src.log import log, warn
from src.client.managers.eventmanager.event import Event

from direct.task import Task

class EventManager:
    def __init__(self, instance):
        self._events = {}
        self.instance = instance

        instance.spawnNewTask()

    def poll(self, task):
        for eventName in self._events:
            event = self._events[eventName]

            if event.triggered:
                log("Event [{}] was triggered!".format(eventName), "Worker/EventManager")
                event.reset()

            return Task.cont

    def create_new_event(self, name = "Hello, World!", description = "Lorem Ipsum Door Sit"):
        event = Event(name, description)
        self._events.update({name: event})