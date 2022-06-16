import typer
from python_library_azure.services.logger import Logger
from typing import Optional
from snapcleanup.config import settings
from snapcleanup.core import DiskSnapshotCleanup


app = typer.Typer(help="Azure Disk Snapshot Cleanup", no_args_is_help=True)
snap_cleanup = DiskSnapshotCleanup()
logger = Logger()


@app.command("list-sub")
def list_subscriptions(
    csv: Optional[str] = typer.Option(default=None, help="CSV file path to export data"),
    json: Optional[str] = typer.Option(default=None, help="JSON file path to export data"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Show more logs"),
):
    """List all subscriptions that user has access."""
    list_subscription = snap_cleanup.get_list_subscription()
    fields_to_print = {
        "subscription_id": "Subscription ID",
        "name": "Subscription Name"
    }
    fields_to_export = ["subscription_id", "name", "tags"]
    logger.print_table(
        table_title="Subscription List",
        headers=fields_to_print,
        object_list=list_subscription,
    )
    if isinstance(csv, str):
        logger.create_csv_file(
            file_path=csv,
            headers=fields_to_export,
            object_list=list_subscription,
            delimiter=";",
            verbose=verbose,
        )
    if isinstance(json, str):
        logger.create_json_file(
            file_path=json,
            headers=fields_to_export,
            object_list=list_subscription,
            indent_spaces=4,
            verbose=verbose,
        )


@app.command("list-rg")
def list_resource_groups(
    csv: Optional[str] = typer.Option(default=None, help="CSV file path to export data"),
    json: Optional[str] = typer.Option(default=None, help="JSON file path to export data"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Show more logs"),
):
    """List all resource groups."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_IDS:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        list_resource_group = snap_cleanup.get_list_resource_group(subscription_id)
        fields_to_print = {
            "name": "Resource Group Name",
            "location": "Location"
        }
        fields_to_export = ["subscription_id", "resource_group_id", "name", "location", "tags", "resource_type"]
        logger.print_table(
            table_title=f"Resource Group List: {subscription_info.name}",
            headers=fields_to_print,
            object_list=list_resource_group,
        )
        if isinstance(csv, str):
            logger.create_csv_file(
                file_path=csv,
                headers=fields_to_export,
                object_list=list_resource_group,
                delimiter=";",
                verbose=verbose,
            )
        if isinstance(json, str):
            logger.create_json_file(
                file_path=json,
                headers=fields_to_export,
                object_list=list_resource_group,
                indent_spaces=4,
                verbose=verbose,
            )


@app.command("list-snap")
def list_snapshots(
    csv: Optional[str] = typer.Option(default=None, help="CSV file path to export data"),
    json: Optional[str] = typer.Option(default=None, help="JSON file path to export data"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Show more logs"),
):
    """List all snapshots."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_IDS:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        list_snapshot = snap_cleanup.get_list_disk_snapshot(subscription_id)
        fields_to_print = {
            "resource_group_name": "Resource Group Name",
            "name": "Snapshot Name",
            "location": "Location",
            "created_date": "Created Date",
            "ttl_tag_value": f"Tag: {settings.TTL.TAG_NAME}"
        }
        fields_to_export = ["subscription_id", "resource_group_name", "snapshot_id", "name", "location", "tags", "resource_type", "created_date"]
        logger.print_table(
            table_title=f"Snapshot List: {subscription_info.name}",
            headers=fields_to_print,
            object_list=list_snapshot,
        )
        if isinstance(csv, str):
            logger.create_csv_file(
                file_path=csv,
                headers=fields_to_export,
                object_list=list_snapshot,
                delimiter=";",
                verbose=verbose,
            )
        if isinstance(json, str):
            logger.create_json_file(
                file_path=json,
                headers=fields_to_export,
                object_list=list_snapshot,
                indent_spaces=4,
                verbose=verbose,
            )


@app.command("update-snap-tag")
def update_snap_tag(
    csv: Optional[str] = typer.Option(default=None, help="CSV file path to export data"),
    json: Optional[str] = typer.Option(default=None, help="JSON file path to export data"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Show more logs"),
    ttl_tag_name: Optional[str] = typer.Option(
        default=settings.TTL.TAG_NAME, help="Name of time-to-live tag"
    ),
    ttl_days: Optional[int] = typer.Option(
        default=settings.TTL.DAYS_BY_DEFAULT, help="Days to time-to-live tag"
    ),
    dry_run: Optional[bool] = typer.Option(default=False, help="Command simulation"),
):
    """Add time-to-live tag on snapshots that do not already have."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_IDS:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        list_snapshot = snap_cleanup.get_list_disk_snapshot(subscription_id)
        updated_list_snapshot = snap_cleanup.update_snapshot_tag(
            subscription_id=subscription_id,
            list_snapshot=list_snapshot,
            ttl_tag_name=ttl_tag_name,
            ttl_days=ttl_days,
            dry_run=dry_run,
        )
        fields_to_print = {
            "resource_group_name": "Resource Group Name",
            "name": "Snapshot Name",
            "location": "Location",
            "created_date": "Created Date",
            "ttl_tag_value": f"Tag: {settings.TTL.TAG_NAME}",
            "action": "Action"
        }
        fields_to_export = ["subscription_id", "resource_group_name", "snapshot_id", "name", "location", "tags", "resource_type", "created_date"]
        logger.print_table(
            table_title=f"Updated Snapshots: {subscription_info.name}",
            headers=fields_to_print,
            object_list=updated_list_snapshot,
        )
        if isinstance(csv, str):
            logger.create_csv_file(
                file_path=csv,
                headers=fields_to_export,
                object_list=updated_list_snapshot,
                delimiter=";",
                verbose=verbose,
            )
        if isinstance(json, str):
            logger.create_json_file(
                file_path=json,
                headers=fields_to_export,
                object_list=updated_list_snapshot,
                indent_spaces=4,
                verbose=verbose,
            )


@app.command("delete-snap")
def delete_snap_tag(
    csv: Optional[str] = typer.Option(default=None, help="CSV file path to export data"),
    json: Optional[str] = typer.Option(default=None, help="JSON file path to export data"),
    verbose: Optional[bool] = typer.Option(False, "--verbose", "-v", help="Show more logs"),
    dry_run: Optional[bool] = typer.Option(default=False, help="Command simulation"),
):
    """Delete all Add time-to-live tag on snapshots that do not already have."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_IDS:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        list_snapshot = snap_cleanup.get_list_disk_snapshot(subscription_id)
        deleted_list_snapshot = snap_cleanup.delete_snapshot(
            subscription_id=subscription_id,
            list_snapshot=list_snapshot,
            dry_run=dry_run
        )
        fields_to_print = {
            "resource_group_name": "Resource Group Name",
            "name": "Snapshot Name",
            "location": "Location",
            "created_date": "Created Date",
            "ttl_tag_value": f"Tag: {settings.TTL.TAG_NAME}",
            "action": "Action"
        }
        fields_to_export = ["subscription_id", "resource_group_name", "snapshot_id", "name", "location", "tags", "resource_type", "created_date"]
        logger.print_table(
            table_title=f"Deleted Snapshots: {subscription_info.name}",
            headers=fields_to_print,
            object_list=deleted_list_snapshot,
        )
        if isinstance(csv, str):
            logger.create_csv_file(
                file_path=csv,
                headers=fields_to_export,
                object_list=deleted_list_snapshot,
                delimiter=";",
                verbose=verbose,
            )
        if isinstance(json, str):
            logger.create_json_file(
                file_path=json,
                headers=fields_to_export,
                object_list=deleted_list_snapshot,
                indent_spaces=4,
                verbose=verbose,
            )
