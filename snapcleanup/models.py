from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from .config import settings


@dataclass(frozen=True)
class ActionStates(Enum):
    NOT_DEFINED = 'Not Defined'
    PENDING_UPDATE = 'Pending Update'
    UPDATED = 'Updated'
    PENDING_DELETE = 'Pending Delete'
    DELETED = 'Deleted'


@dataclass(frozen=True)
class SubscriptionInfo:
    id: str
    name: str


@dataclass(frozen=True)
class ResourceGroupInfo:
    name: str
    location: str


@dataclass(frozen=True)
class SnapshotInfo:
    resource_group: str
    name: str
    location: str
    dt_created: datetime
    tags: dict = field(default_factory=dict)
    action: ActionStates = field(init=False, default_factory=ActionStates.NOT_DEFINED)

    @property
    def ttl_tag_value(self):
        tag_name = settings.TTL.TAG_NAME
        if isinstance(self.__tags, dict):
            if isinstance(self.__tags.get(tag_name), str):
                return self.__tags.get(tag_name)
            return ''
        return ''
