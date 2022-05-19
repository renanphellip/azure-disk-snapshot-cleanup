from datetime import datetime, timedelta
from snapcleanup.config import settings
from snapcleanup.azure.resource_group import ResourceGroupService
from snapcleanup.entities import (
    ActionStates,
    ResourceGroupInfo,
    SubscriptionInfo,
)
from snapcleanup.azure.azure import AzureService
from snapcleanup.azure.subscription import SubscriptionService
from snapcleanup.azure.snapshot import SnapshotService
from snapcleanup.entities import SnapshotInfo
from rich.console import Console


class DiskSnapshotCleanup:
    def __init__(self, client_id: str, client_secret: str, tenant_id: str) -> None:
        if settings.AZURE_CORE_ONLY_SHOW_ERRORS == True:
            AzureService.config_only_show_errors()
        AzureService.login(client_id, client_secret, tenant_id)
        self.console = Console()

    def set_subscription(self, subscription_id: str) -> bool:
        return SubscriptionService.set_subscription(subscription_id)

    def list_subscriptions(self) -> list[SubscriptionInfo]:
        with self.console.status("Listing subscriptions..."):
            return SubscriptionService.list_subscriptions()

    def get_subscription(self, subscription_id: str) -> SubscriptionInfo:
        return SubscriptionService.get_subscription(subscription_id)

    def list_resource_groups(self) -> list[ResourceGroupInfo]:
        with self.console.status("Listing resource groups..."):
            return ResourceGroupService.list_resource_groups()

    def list_snapshots(self) -> list[SnapshotInfo]:
        with self.console.status("Listing snapshots..."):
            return SnapshotService.list_snapshots()

    def update_snapshot_tag(
        self,
        list_snapshots: list[SnapshotInfo],
        ttl_tag_name: str,
        ttl_days: int,
        dry_run: bool,
    ) -> list[SnapshotInfo]:
        with self.console.status("Updating snapshots..."):
            list_snapshot_id: list[str] = []
            for snapshot in list_snapshots:
                if snapshot.ttl_tag_exists:
                    snapshot.action = ActionStates.UPDATED
                else:
                    snapshot.action = ActionStates.PENDING_UPDATE
                    list_snapshot_id.append(snapshot.snapshot_id)

            if dry_run == False:
                future_date = (datetime.today() + timedelta(days=ttl_days)).strftime("%Y-%m-%d")
                ttl_tag = {ttl_tag_name: future_date}
                result = SnapshotService.update_snapshot_tags(list_snapshot_id, ttl_tag)
                if result:
                    for snapshot in list_snapshots:
                        if snapshot.snapshot_id in list_snapshot_id:
                            snapshot.tags.update(ttl_tag)
                            snapshot.action = ActionStates.UPDATED

            return list_snapshots

    def delete_snapshots(
        self, list_snapshots: list[SnapshotInfo], dry_run: bool
    ) -> list[SnapshotInfo]:
        with self.console.status("Deleting snapshots..."):
            list_snapshot_id: list[str] = []
            for snapshot in list_snapshots:
                if snapshot.ttl_tag_exists:
                    ttl_date = snapshot.ttl_tag_value
                    today = datetime.today().strftime("%Y-%m-%d")
                    if ttl_date < today:
                        snapshot.action = ActionStates.PENDING_DELETE
                        list_snapshot_id.append(snapshot.snapshot_id)

            if dry_run == False:
                result = SnapshotService.delete_snapshot(list_snapshot_id)
                if result:
                    for snapshot in list_snapshots:
                        if snapshot.snapshot_id in list_snapshot_id:
                            snapshot.action = ActionStates.DELETED

            return list_snapshots
