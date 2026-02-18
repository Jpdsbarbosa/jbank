from abc import ABC, abstractmethod
from typing import List

from ...domain.events import DomainEvent

class EventPublisher(ABC):

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    async def publish_many(self, events: List[DomainEvent]) -> None:
        pass