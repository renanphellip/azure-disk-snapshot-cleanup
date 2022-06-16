from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from snapcleanup.entities import ActionStates, SnapshotInfo
from python_library_azure.entities.subscription import SubscriptionInfo
from python_library_azure.entities.resource_group import ResourceGroupInfo
from python_library_azure.services.subscription import SubscriptionService
from python_library_azure.services.resource_group import ResourceGroupService
from python_library_azure.services.disk_snapshot import DiskSnapshotService
from rich.console import Console


class DiskSnapshotCleanup:
    def __init__(self) -> None:
        self.__credential = DefaultAzureCredential()
        self.__console = Console()

    def get_list_subscription(self) -> list[SubscriptionInfo]:
        with self.__console.status("Listing subscriptions..."):
            subscription_service = SubscriptionService(self.__credential)
            return subscription_service.get_list_subscription()

    def get_subscription(self, subscription_id: str) -> SubscriptionInfo:
        with self.__console.status("Getting subscription..."):
            subscription_service = SubscriptionService(self.__credential)
            return subscription_service.get_subscription(subscription_id)

    def get_list_resource_group(self, subscription_id: str) -> list[ResourceGroupInfo]:
        with self.__console.status("Listing resource groups..."):
            rg_service = ResourceGroupService(self.__credential, subscription_id)
            return rg_service.get_list_resource_group()

    # DiskSnapshotInfo != SnapshotInfo, then we need return a new list
    def get_list_disk_snapshot(self, subscription_id: str) -> list[SnapshotInfo]:
        with self.__console.status("Listing snapshots..."):
            snap_service = DiskSnapshotService(self.__credential, subscription_id)
            list_disk_snapshot = snap_service.get_list_disk_snapshot()
            list_snapshot = []
            for disk_snapshot in list_disk_snapshot:
                list_snapshot.append(SnapshotInfo(
                    subscription_id=disk_snapshot.subscription_id,
                    resource_group_name=disk_snapshot.resource_group_name,
                    snapshot_id=disk_snapshot.snapshot_id,
                    name=disk_snapshot.name,
                    location=disk_snapshot.location,
                    tags=disk_snapshot.tags,
                    resource_type=disk_snapshot.resource_type,
                    created_date=disk_snapshot.created_date
                ))
            return list_snapshot

    def update_snapshot_tag(
        self,
        subscription_id: str,
        list_snapshot: list[SnapshotInfo],
        ttl_tag_name: str,
        ttl_days: int,
        dry_run: bool
    ) -> list[SnapshotInfo]:
        with self.__console.status("Updating snapshots..."):
            for snapshot in list_snapshot:
                if snapshot.ttl_tag_exists:
                    snapshot.action = ActionStates.UPDATED
                else:
                    snapshot.action = ActionStates.PENDING_UPDATE

            if dry_run == False:
                future_date = (datetime.today() + timedelta(days=ttl_days)).strftime("%Y-%m-%d")
                ttl_tag = {ttl_tag_name: future_date}
                snap_service = DiskSnapshotService(self.__credential, subscription_id)
                for snapshot in list_snapshot:
                    if snapshot.action == ActionStates.PENDING_UPDATE:
                        result = snap_service.update_disk_snapshot_tag(
                            resource_group_name=snapshot.resource_group_name,
                            disk_snapshot_name=snapshot.name,
                            updated_tag=ttl_tag
                        )
                        if result:
                            snapshot.tags.update(ttl_tag)
                            snapshot.action = ActionStates.UPDATED

            return list_snapshot

    def delete_snapshot(
        self,
        subscription_id: str,
        list_snapshot: list[SnapshotInfo],
        dry_run: bool
    ) -> list[SnapshotInfo]:
        with self.__console.status("Deleting snapshots..."):
            for snapshot in list_snapshot:
                if snapshot.ttl_tag_exists:
                    ttl_date = snapshot.ttl_tag_value
                    today = datetime.today().strftime("%Y-%m-%d")
                    if ttl_date < today:
                        snapshot.action = ActionStates.PENDING_DELETE

            if dry_run == False:
                snap_service = DiskSnapshotService(self.__credential, subscription_id)
                for snapshot in list_snapshot:
                    if snapshot.action == ActionStates.PENDING_DELETE:
                        result = snap_service.delete_snapshot(
                            resource_group_name=snapshot.resource_group_name,
                            disk_snapshot_name=snapshot.name
                        )
                        if result:
                            snapshot.action = ActionStates.DELETED

            return list_snapshot
