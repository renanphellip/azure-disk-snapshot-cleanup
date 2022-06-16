from dataclasses import dataclass, field
import re
from snapcleanup.config import settings
from python_library_azure.entities.disk_snapshot import DiskSnapshotInfo
from python_library_azure.entities.action import ActionStates


@dataclass
class SnapshotInfo(DiskSnapshotInfo):
    action: ActionStates = field(init=False, default=ActionStates.NOT_DEFINED)

    """
        Não devemos inicializar o action para que não haja
        possibilidade de ter um valor != de NOT_DEFINED.
    """

    @property
    def ttl_tag_value(self) -> str:
        tag_name = settings.TTL.TAG_NAME
        return self.tags.get(tag_name, "")

    @property
    def ttl_tag_exists(self) -> bool:
        ttl_pattern = "^[0-9]{4}(-[0-9]{2}){2}$"
        if re.search(ttl_pattern, self.ttl_tag_value):
            return True
        return False
