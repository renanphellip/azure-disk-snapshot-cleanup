from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from config import settings


class ActionStates(Enum):
    NOT_DEFINED = 'Not Defined'
    PENDING_UPDATE = 'Pending Update'
    UPDATED = 'Updated'
    PENDING_DELETE = 'Pending Delete'
    DELETED = 'Deleted'


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
    name: str
    location: str
    dt_created: datetime
    tags: dict = field(default_factory=dict)
    action: ActionStates = field(init=False)


    '''
        Não devemos inicializar o action para que não haja
        possibilidade de ter um valor != de NOT_DEFINED.
    '''
    def __post_init__(self):
        self.action = ActionStates.NOT_DEFINED


    @property
    def ttl_tag_value(self):
        tag_name = settings.TTL.TAG_NAME
        if isinstance(self.tags, dict):
            if isinstance(self.tags.get(tag_name), str):
                return self.tags.get(tag_name)
        return ''


    @property
    def dt_created(self):
        return datetime.strptime(self.dt_created, "%Y-%m-%dT%H:%M:%S.%f%z")
