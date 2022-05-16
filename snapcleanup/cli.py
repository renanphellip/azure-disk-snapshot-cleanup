import typer
from typing import Optional
from snapcleanup.config import settings
from snapcleanup.core import DiskSnapshotCleanup


cli = typer.Typer(help="Azure Disk Snapshot Cleanup", no_args_is_help=True)
snap_cleanup = DiskSnapshotCleanup(
    client_id=settings.AZURE_CLIENT_ID,
    client_secret=settings.AZURE_CLIENT_SECRET,
    tenant_id=settings.AZURE_TENANT_ID
)


@cli.command("list-sub")
def list_subscriptions(
    csv: Optional[str] = typer.Option(
        default=None, help="CSV file path to export data"
    ),
    json: Optional[str] = typer.Option(
        default=None, help="JSON file path to export data"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Show more logs"
    )
):
    """List all subscriptions that user has access."""
    subscriptions = snap_cleanup.list_subscriptions()
    fields = ["subscription_id", "name"]
    snap_cleanup.print_table(
        table_title="Subscription List",
        headers=fields,
        object_list=subscriptions
    )
    if isinstance(csv, str):
        snap_cleanup.create_csv_file(
            file_path=csv,
            headers=fields,
            object_list=subscriptions,
            delimiter=";",
            verbose=verbose
        )
    if isinstance(json, str):
        snap_cleanup.create_json_file(
            file_path=json,
            headers=fields,
            object_list=subscriptions,
            indent_spaces=4,
            verbose=verbose
        )


@cli.command("list-rg")
def list_resource_groups(
    csv: Optional[str] = typer.Option(
        default=None, help="CSV file path to export data"
    ),
    json: Optional[str] = typer.Option(
        default=None, help="JSON file path to export data"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Show more logs"
    )
):
    """List all resource groups."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_ID:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        if snap_cleanup.set_subscription(subscription_id):
            resource_groups = snap_cleanup.list_resource_groups()
            fields = ["name", "location"]
            snap_cleanup.print_table(
                table_title=f"Resource Group List: {subscription_info.name}",
                headers=fields,
                object_list=resource_groups,
            )
            if isinstance(csv, str):
                snap_cleanup.create_csv_file(
                    file_path=csv,
                    headers=fields,
                    object_list=resource_groups,
                    delimiter=";",
                    verbose=verbose
                )
            if isinstance(json, str):
                snap_cleanup.create_json_file(
                    file_path=json,
                    headers=fields,
                    object_list=resource_groups,
                    indent_spaces=4,
                    verbose=verbose
                )


@cli.command("list-snap")
def list_snapshots(
    csv: Optional[str] = typer.Option(
        default=None, help="CSV file path to export data"
    ),
    json: Optional[str] = typer.Option(
        default=None, help="JSON file path to export data"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Show more logs"
    )
):
    """List all snapshots."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_ID:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        if snap_cleanup.set_subscription(subscription_id):
            snapshots = snap_cleanup.list_snapshots()
            fields = [
                "resource_group",
                "name",
                "location",
                "created_date",
                "ttl_tag_value",
            ]
            snap_cleanup.print_table(
                table_title=f"Snapshot List: {subscription_info.name}",
                headers=fields,
                object_list=snapshots,
            )
            if isinstance(csv, str):
                snap_cleanup.create_csv_file(
                    file_path=csv,
                    headers=fields,
                    object_list=snapshots,
                    delimiter=";",
                    verbose=verbose
                )
            if isinstance(json, str):
                snap_cleanup.create_json_file(
                    file_path=json,
                    headers=fields,
                    object_list=snapshots,
                    indent_spaces=4,
                    verbose=verbose
                )


@cli.command("update-snap-tag")
def update_snap_tag(
    csv: Optional[str] = typer.Option(
        default=None, help="CSV file path to export data"
    ),
    json: Optional[str] = typer.Option(
        default=None, help="JSON file path to export data"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Show more logs"
    ),
    ttl_tag_name: Optional[str] = typer.Option(
        default=settings.TTL.TAG_NAME, help="Name of time-to-live tag"
    ),
    ttl_days: Optional[int] = typer.Option(
        default=settings.TTL.DAYS_BY_DEFAULT, help="Days to time-to-live tag"
    ),
    dry_run: Optional[bool] = typer.Option(
        default=False, help="Command simulation"
    ),
):
    """Add time-to-live tag on snapshots that do not already have."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_ID:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        if snap_cleanup.set_subscription(subscription_id):
            snapshots = snap_cleanup.list_snapshots()
            updated_snapshots = snap_cleanup.update_snapshot_tag(
                list_snapshots=snapshots,
                ttl_tag_name=ttl_tag_name,
                ttl_days=ttl_days,
                dry_run=dry_run,
            )
            fields = [
                "resource_group",
                "name",
                "location",
                "created_date",
                "ttl_tag_value",
                "action",
            ]
            snap_cleanup.print_table(
                table_title=f"Updated Snapshots: {subscription_info.name}",
                headers=fields,
                object_list=updated_snapshots,
            )
            if isinstance(csv, str):
                snap_cleanup.create_csv_file(
                    file_path=csv,
                    headers=fields,
                    object_list=updated_snapshots,
                    delimiter=";",
                    verbose=verbose
                )
            if isinstance(json, str):
                snap_cleanup.create_json_file(
                    file_path=json,
                    headers=fields,
                    object_list=updated_snapshots,
                    indent_spaces=4,
                    verbose=verbose
                )


@cli.command("delete-snap")
def delete_snap_tag(
    csv: Optional[str] = typer.Option(
        default=None, help="CSV file path to export data"
    ),
    json: Optional[str] = typer.Option(
        default=None, help="JSON file path to export data"
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="Show more logs"
    ),
    dry_run: Optional[bool] = typer.Option(
        default=False, help="Command simulation"
    ),
):
    """Delete all Add time-to-live tag on snapshots that do not already have."""
    for subscription_id in settings.AZURE_SUBSCRIPTION_ID:
        subscription_info = snap_cleanup.get_subscription(subscription_id)
        if snap_cleanup.set_subscription(subscription_id):
            snapshots = snap_cleanup.list_snapshots()
            deleted_snapshots = snap_cleanup.delete_snapshots(
                list_snapshots=snapshots, dry_run=dry_run
            )
            fields = [
                "resource_group",
                "name",
                "location",
                "created_date",
                "ttl_tag_value",
                "action",
            ]
            snap_cleanup.print_table(
                table_title=f"Deleted Snapshots: {subscription_info.name}",
                headers=fields,
                object_list=deleted_snapshots,
            )
            if isinstance(csv, str):
                snap_cleanup.create_csv_file(
                    file_path=csv,
                    headers=fields,
                    object_list=deleted_snapshots,
                    delimiter=";",
                    verbose=verbose
                )
            if isinstance(json, str):
                snap_cleanup.create_json_file(
                    file_path=json,
                    headers=fields,
                    object_list=deleted_snapshots,
                    indent_spaces=4,
                    verbose=verbose
                )
