import re
from datetime import datetime, timedelta
from snapcleanup.config import settings
from snapcleanup.azure.resource_group import ResourceGroupService
from snapcleanup.entities import ActionStates, ResourceGroupInfo, SubscriptionInfo
from snapcleanup.azure.azure import AzureService
from snapcleanup.azure.subscription import SubscriptionService
from snapcleanup.azure.snapshot import SnapshotService
from snapcleanup.entities import SnapshotInfo
from rich.table import Table
from rich.console import Console


class DiskSnapshotCleanup:

    def __init__(self, client_id: str, client_secret: str, tenant_id: str, subscription_id: str) -> None:
        if settings.AZURE_CORE_ONLY_SHOW_ERRORS == True:
            AzureService.config_only_show_errors()
        AzureService.login(client_id, client_secret, tenant_id)
        SubscriptionService.set_subscription(subscription_id)
        self.console = Console()


    def __validate_ttl_tag_pattern(self, ttl_tag_value: str) -> bool:
        ttl_pattern = '^[0-9]{4}(-[0-9]{2}){2}$'
        if re.search(ttl_pattern, ttl_tag_value):
            return True
        return False
    

    def print_table(self, table_title: str, headers: list[str], object_list: list[object]) -> Table:
        try:
            table = Table(title=f"[bold]{table_title}[/]")
            for header in headers:
                table.add_column(header)
            for item in object_list:
                values = [str(getattr(item, header)) for header in headers]
                table.add_row(*values)
            self.console.print("\n", table, "\n")
            return table
        except AttributeError:
            raise AttributeError(f'The table headers must be equivalent object attributes name.')


    def list_subscriptions(self) -> list[SubscriptionInfo]:
        return SubscriptionService.list_subscriptions()


    def list_resource_groups(self) -> list[ResourceGroupInfo]:
        return ResourceGroupService.list_resource_groups()


    def list_snapshots(self) -> list[SnapshotInfo]:
        return SnapshotService.list_snapshots()


    def update_snapshot_tag(self, list_snapshots: list[SnapshotInfo], ttl_tag_name: str, ttl_days: int, dry_run: bool) -> list[SnapshotInfo]:
        list_snapshot_id: list[str] = []
        for snapshot in list_snapshots:
            if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
                snapshot.action = ActionStates.UPDATED
            else:
                snapshot.action = ActionStates.PENDING_UPDATE
                list_snapshot_id.append(snapshot.snapshot_id)

        if dry_run == False:
            future_date = ( datetime.today() + timedelta(days=ttl_days) ).strftime('%Y-%m-%d')
            ttl_tag = {
                ttl_tag_name: future_date
            }
            result = SnapshotService.update_snapshot_tags(list_snapshot_id, ttl_tag)
            if result:
                for snapshot in list_snapshots:
                    if snapshot.snapshot_id in list_snapshot_id:
                        snapshot.tags.update(ttl_tag)
                        snapshot.action = ActionStates.UPDATED
                        
        return list_snapshots


    def delete_snapshots(self, list_snapshots: list[SnapshotInfo], dry_run: bool) -> list[SnapshotInfo]:
        list_snapshot_id: list[str] = []
        for snapshot in list_snapshots:
            if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
                ttl_date = snapshot.ttl_tag_value
                today = datetime.today().strftime('%Y-%m-%d')
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
