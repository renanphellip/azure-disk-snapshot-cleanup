import re
import os
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
from rich.table import Table
from rich.console import Console
from prettytable import PrettyTable


class DiskSnapshotCleanup:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        tenant_id: str
    ) -> None:
        if settings.AZURE_CORE_ONLY_SHOW_ERRORS == True:
            AzureService.config_only_show_errors()
        AzureService.login(client_id, client_secret, tenant_id)
        self.console = Console()


    def __validate_ttl_tag_pattern(self, ttl_tag_value: str) -> bool:
        ttl_pattern = "^[0-9]{4}(-[0-9]{2}){2}$"
        if re.search(ttl_pattern, ttl_tag_value):
            return True
        return False


    def __create_pretty_table(
        self, headers: list[str], object_list: list[object]
    ):
        """
        This private method its used only to create a PrettyTable to
        facilitate exporting data to JSON files
        """
        try:
            table = PrettyTable(headers)
            for item in object_list:
                values = [str(getattr(item, header)) for header in headers]
                table.add_row(values)
            return table
        except AttributeError:
            self.console.print(
                f"The table headers must be equivalent object attributes name.",
                style="red",
            )
            exit(1)
        except Exception as error:
            self.console.print(error, style="red")
            exit(1)

    
    def print_table(
        self, table_title: str, headers: list[str], object_list: list[object]
    ) -> Table:
        try:
            with self.console.status('Creating table...'):
                table = Table(title=f"[bold]{table_title}[/]")
                for header in headers:
                    table.add_column(header)
                for item in object_list:
                    values = [str(getattr(item, header)) for header in headers]
                    table.add_row(*values)
                self.console.print("\n", table)
                return table
        except AttributeError:
            self.console.print(
                f"The table headers must be equivalent object attributes name.",
                style="red",
            )
            exit(1)
        except Exception as error:
            self.console.print(error, style="red")
            exit(1)

    
    def create_csv_file(
        self,
        file_path: str,
        headers: list[str],
        object_list: list[object],
        delimiter: str,
        verbose: bool,
    ) -> bool:
        try:
            with self.console.status('Creating CSV file...'):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file=file_path, mode="w", encoding="utf-8") as csv_file:
                    fields = delimiter.join(headers) + "\n"
                    csv_file.write(fields)
                    for item in object_list:
                        values = [str(getattr(item, header)) for header in headers]
                        row_values = delimiter.join(values) + "\n"
                        csv_file.write(row_values)
                self.console.print(f"{file_path} has been created.", style="green")
        except Exception as error:
            self.console.print(f"Failed to create: {file_path}", style="red")
            if verbose:
                self.console.print(f"Exception: {error}", style="red")
            exit(1)

    
    def create_json_file(
        self,
        file_path: str,
        headers: list[str],
        object_list: list[object],
        indent_spaces: int,
        verbose: bool,
    ) -> bool:
        table = self.__create_pretty_table(headers, object_list)
        json_string = table.get_json_string(header=False, indent=indent_spaces)
        try:
            with self.console.status('Creating JSON file...'):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file=file_path, mode="w", encoding="utf-8") as json_file:
                    json_file.write(json_string)
                self.console.print(f"{file_path} has been created.", style="green")
        except Exception as error:
            self.console.print(f"Failed to create: {file_path}", style="red")
            if verbose:
                self.console.print(f"Exception: {error}", style="red")
            exit(1)
    

    def set_subscription(self, subscription_id: str) -> bool:
        return SubscriptionService.set_subscription(subscription_id)

    
    def list_subscriptions(self) -> list[SubscriptionInfo]:
        with self.console.status('Listing subscriptions...'):
            return SubscriptionService.list_subscriptions()
    

    def get_subscription(self, subscription_id: str) -> SubscriptionInfo:
        return SubscriptionService.get_subscription(subscription_id)

    
    def list_resource_groups(self) -> list[ResourceGroupInfo]:
        with self.console.status('Listing resource groups...'):
            return ResourceGroupService.list_resource_groups()

    
    def list_snapshots(self) -> list[SnapshotInfo]:
        with self.console.status('Listing snapshots...'):
            return SnapshotService.list_snapshots()

    
    def update_snapshot_tag(
        self,
        list_snapshots: list[SnapshotInfo],
        ttl_tag_name: str,
        ttl_days: int,
        dry_run: bool,
    ) -> list[SnapshotInfo]:
        with self.console.status('Updating snapshots...'):
            list_snapshot_id: list[str] = []
            for snapshot in list_snapshots:
                if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
                    snapshot.action = ActionStates.UPDATED
                else:
                    snapshot.action = ActionStates.PENDING_UPDATE
                    list_snapshot_id.append(snapshot.snapshot_id)

            if dry_run == False:
                future_date = (
                    datetime.today() + timedelta(days=ttl_days)
                ).strftime("%Y-%m-%d")
                ttl_tag = {ttl_tag_name: future_date}
                result = SnapshotService.update_snapshot_tags(
                    list_snapshot_id, ttl_tag
                )
                if result:
                    for snapshot in list_snapshots:
                        if snapshot.snapshot_id in list_snapshot_id:
                            snapshot.tags.update(ttl_tag)
                            snapshot.action = ActionStates.UPDATED

            return list_snapshots

    
    def delete_snapshots(
        self, list_snapshots: list[SnapshotInfo], dry_run: bool
    ) -> list[SnapshotInfo]:
        with self.console.status('Deleting snapshots...'):
            list_snapshot_id: list[str] = []
            for snapshot in list_snapshots:
                if self.__validate_ttl_tag_pattern(snapshot.ttl_tag_value):
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
