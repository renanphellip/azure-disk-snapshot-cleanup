from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import re
from snapcleanup.config import settings


class ActionStates(Enum):
    NOT_DEFINED = "Not Defined"
    PENDING_UPDATE = "Pending Update"
    UPDATED = "Updated"
    PENDING_DELETE = "Pending Delete"
    DELETED = "Deleted"

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
    """
    :param: created_date = "2022-12-30T12:30:50.123456-0300"
    """

    resource_group: str
    snapshot_id: str
    name: str
    location: str
    created_date: str
    tags: dict = field(default_factory=dict)
    action: ActionStates = field(init=False)

    """
        Não devemos inicializar o action para que não haja
        possibilidade de ter um valor != de NOT_DEFINED.
    """

    def __post_init__(self):
        self.action = ActionStates.NOT_DEFINED
        input_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        output_format = "%Y-%m-%d %H:%M:%S"
        created_datetime = datetime.strptime(self.created_date, input_format)
        self.created_date = created_datetime.strftime(output_format)

    @property
    def ttl_tag_value(self):
        tag_name = settings.TTL.TAG_NAME
        if isinstance(self.tags, dict):
            if isinstance(self.tags.get(tag_name), str):
                return self.tags.get(tag_name)
        return ""

    @property
    def ttl_tag_exists(self):
        ttl_pattern = "^[0-9]{4}(-[0-9]{2}){2}$"
        if re.search(ttl_pattern, self.ttl_tag_value):
            return True
        return False
