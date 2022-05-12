import re
from datetime import datetime, timedelta
from snapcleanup.config import settings
from snapcleanup.azure.resource_group import ResourceGroupService
from snapcleanup.entities import ActionStates
from snapcleanup.azure.azure import AzureService
from snapcleanup.azure.subscription import SubscriptionService
from snapcleanup.azure.snapshot import SnapshotService
from snapcleanup.entities import SnapshotInfo
from rich.table import Table


class DiskSnapshotCleanup:

    def __init__(self, client_id: str, client_secret: str, tenant_id: str, subscription_id: str) -> None:
        AzureService.login(client_id, client_secret, tenant_id)
        SubscriptionService.set_subscription(subscription_id)


    def __validate_ttl_tag_pattern(self, ttl_tag_value: str) -> bool:
        ttl_pattern = '^[0-9]{4}(-[0-9]{2}){2}$'
        if re.search(ttl_pattern, ttl_tag_value):
            return True
        return False


    def list_subscriptions(self) -> Table:
        subscriptions = SubscriptionService.list_subscriptions()
        table = Table(title="Subscription List")
        headers = ["ID", "Name"]
        for header in headers:
            table.add_column(header, style="magenta")
        for subscription in subscriptions:
            table.add_row(subscription.subscription_id, subscription.name)
        return table


    def list_resource_groups(self) -> Table:
        resource_groups = ResourceGroupService.list_resource_groups()
        table = Table(title="Resource Group List")
        headers = ["Name", "Location"]
        for header in headers:
            table.add_column(header, style="magenta")
        for resource_group in resource_groups:
            table.add_row(resource_group.name, resource_group.location)
        return table


    def list_snapshots(self) -> Table:
        snapshots = SnapshotService.list_snapshots()
        table = Table(title="Snapshot List")
        headers = ["Resource Group", "Snapshot", "Location", "Created Date", f"{settings.TTL.TAG_NAME} Tag"]
        for header in headers:
            table.add_column(header, style="magenta")
        for snapshot in snapshots:
            table.add_row(
                snapshot.resource_group,
                snapshot.name,
                snapshot.location,
                snapshot.dt_created,
                snapshot.ttl_tag_value
            )
        return table


    def update_snapshot_tag(self, list_snapshots: list[SnapshotInfo], ttl_tag_name: str, ttl_days: int, dry_run: bool) -> Table:
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
        
        table = Table(title="Updated Snapshots")
        headers = ["Resource Group", "Snapshot", "Location", "Created Date", f"{settings.TTL.TAG_NAME} Tag", "Action"]
        for header in headers:
            table.add_column(header, style="magenta")
        for snapshot in list_snapshots:
            table.add_row(
                snapshot.resource_group,
                snapshot.name,
                snapshot.location,
                snapshot.dt_created,
                snapshot.ttl_tag_value,
                snapshot.action
            )
        return table


    def delete_snapshots(self, list_snapshots: list[SnapshotInfo], dry_run: bool) -> Table:
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
        
        table = Table(title="Deleted Snapshots")
        headers = ["Resource Group", "Snapshot", "Location", "Created Date", f"{settings.TTL.TAG_NAME} Tag", "Action"]
        for header in headers:
            table.add_column(header, style="magenta")
        for snapshot in list_snapshots:
            table.add_row(
                snapshot.resource_group,
                snapshot.name,
                snapshot.location,
                snapshot.dt_created,
                snapshot.ttl_tag_value,
                snapshot.action
            )
        return table
