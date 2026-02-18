from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

@dataclass(frozen=True)
class DomainEvent:

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.now)
    event_type: str = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_type", self.__class__.__name__)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "occurred_at": self.occurred_at,
            "event_type": self.event_type,
        }