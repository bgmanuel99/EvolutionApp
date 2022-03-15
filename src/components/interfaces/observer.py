from abc import ABC, abstractmethod

class Observer(ABC):

    """The Observer interface declares the update method, used by the subscribers"""

    @abstractmethod
    def update(self, *args) -> None:
        """Receive the update from the publisher"""
        pass