from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from snapcleanup.config import settings


class ActionStates(Enum):
    NOT_DEFINED = 'Not Defined'
    PENDING_UPDATE = 'Pending Update'
    UPDATED = 'Updated'
    PENDING_DELETE = 'Pending Delete'
    DELETED = 'Deleted'

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class SubscriptionInfo:
    subscription_id: str
    name: str


@dataclass(frozen=True)
class ResourceGroupInfo:
    name: str
    location: str


@dataclass
class SnapshotInfo:
    resource_group: str
    snapshot_id: str
    name: str
    location: str
    created_date: Any
    tags: dict = field(default_factory=dict)
    action: ActionStates = field(init=False)


    '''
        Não devemos inicializar o action para que não haja
        possibilidade de ter um valor != de NOT_DEFINED.
    '''
    def __post_init__(self):
        self.action = ActionStates.NOT_DEFINED
        self.created_date = datetime.strptime(self.created_date, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")


    @property
    def ttl_tag_value(self):
        tag_name = settings.TTL.TAG_NAME
        if isinstance(self.tags, dict):
            if isinstance(self.tags.get(tag_name), str):
                return self.tags.get(tag_name)
        return ''
