from collections import defaultdict


class EventBus:
    _listeners = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type, handler):
        cls._listeners[event_type].append(handler)

    @classmethod
    def dispatch(cls, event):
        for handler in cls._listeners[type(event)]:
            handler(event)
