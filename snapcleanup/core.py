import re
from datetime import datetime, timedelta
from typing import Literal
from snapcleanup.azure.resource_group import ResourceGroupService
from snapcleanup.entities import ActionStates
from snapcleanup.azure.azure import AzureService
from snapcleanup.azure.subscription import SubscriptionService
from snapcleanup.azure.snapshot import SnapshotService
from snapcleanup.entities import SnapshotInfo


class DiskSnapshotCleanup:

    def __init__(self, client_id: str, client_secret: str, tenant_id: str, subscription_id: str) -> None:
        AzureService.login(client_id, client_secret, tenant_id)
        SubscriptionService.set_subscription(subscription_id)


    def __validate_ttl_tag_pattern(self, ttl_tag_value: str) -> bool:
        ttl_pattern = '^[0-9]{4}(-[0-9]{2}){2}$'
        if re.search(ttl_pattern, ttl_tag_value):
            return True
        return False


    def list_subscriptions(self):
        return SubscriptionService.list_subscriptions()


    def list_snapshots(self):
        return ResourceGroupService.list_resource_groups()


    def list_snapshots(self):
        return SnapshotService.list_snapshots()


    def update_snapshot_tag(self, list_snapshots: list[SnapshotInfo], ttl_tag_name: str, ttl_days: int, dry_run: bool) -> list[SnapshotInfo]:
        for snapshot in list_snapshots:
            if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
                snapshot.action = ActionStates.UPDATED
            else:
                snapshot.action = ActionStates.PENDING_UPDATE
                if dry_run == False:
                    future_date = ( datetime.today() + timedelta(days=ttl_days) ).strftime('%Y-%m-%d')
                    ttl_tag = {
                        ttl_tag_name: future_date
                    }
                    result = SnapshotService.update_snapshot_tags(snapshot.id, ttl_tag)
                    if result:
                        snapshot.tags.update(ttl_tag)
                        snapshot.action = ActionStates.UPDATED
        return list_snapshots


    def delete_snapshots(self, list_snapshots: list[SnapshotInfo], dry_run: bool) -> list[SnapshotInfo]:
        for snapshot in list_snapshots:
            if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
                ttl_date = snapshot.ttl_tag_value
                today = datetime.today().strftime('%Y-%m-%d')
                if ttl_date < today:
                    snapshot.action = ActionStates.PENDING_DELETE
                    if dry_run == False:
                        result = SnapshotService.delete_snapshot(snapshot.id)
                        if result:
                            snapshot.action = ActionStates.DELETED
        return list_snapshots
