from abc import ABC, abstractmethod

class Publisher(ABC):

    """The publisher interface declares a set of methods for managing subscribers"""

    @abstractmethod
    def subscribe(self, observer) -> None:
        """Subscribes an observer to the publisher"""
        pass

    @abstractmethod
    def unsubscribe(self, observer) -> None:
        """Unsubscribe an observer from the publisher"""
        pass

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event"""
        pass