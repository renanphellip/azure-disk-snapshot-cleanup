import typer
from typing import Optional
from snapcleanup.config import settings
from snapcleanup.core import DiskSnapshotCleanup


cli = typer.Typer(help="Azure Disk Snapshot Cleanup", no_args_is_help=True)
snap_cleanup = DiskSnapshotCleanup(
    client_id=settings.AZURE_CLIENT_ID,
    client_secret=settings.AZURE_CLIENT_SECRET,
    tenant_id=settings.AZURE_TENANT_ID,
    subscription_id=settings.AZURE_SUBSCRIPTION_ID,
)


@cli.command("list-sub")
def list_subscriptions(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    ),
):
    """List all subscriptions that user has access."""
    subscriptions = snap_cleanup.list_subscriptions()
    snap_cleanup.print_table(
        table_title="Subscription List",
        headers=["subscription_id", "name"],
        object_list=subscriptions,
    )


@cli.command("list-rg")
def list_resource_groups(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    ),
):
    """List all resource groups."""
    resource_groups = snap_cleanup.list_resource_groups()
    snap_cleanup.print_table(
        table_title="Resource Group List",
        headers=["name", "location"],
        object_list=resource_groups,
    )


@cli.command("list-snap")
def list_snapshots(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    ),
):
    """List all snapshots."""
    snapshots = snap_cleanup.list_snapshots()
    snap_cleanup.print_table(
        table_title="Snapshot List",
        headers=[
            "resource_group",
            "name",
            "location",
            "created_date",
            "ttl_tag_value",
        ],
        object_list=snapshots,
    )


@cli.command("update-snap-tag")
def update_snap_tag(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
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
    snapshots = snap_cleanup.list_snapshots()
    updated_snapshots = snap_cleanup.update_snapshot_tag(
        list_snapshots=snapshots,
        ttl_tag_name=ttl_tag_name,
        ttl_days=ttl_days,
        dry_run=dry_run,
    )
    snap_cleanup.print_table(
        table_title="Updated Snapshots",
        headers=[
            "resource_group",
            "name",
            "location",
            "created_date",
            "ttl_tag_value",
            "action",
        ],
        object_list=updated_snapshots,
    )


@cli.command("delete-snap")
def delete_snap_tag(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    ),
    dry_run: Optional[bool] = typer.Option(
        default=False, help="Command simulation"
    ),
):
    """Delete all Add time-to-live tag on snapshots that do not already have."""
    snapshots = snap_cleanup.list_snapshots()
    deleted_snapshots = snap_cleanup.delete_snapshots(
        list_snapshots=snapshots, dry_run=dry_run
    )
    snap_cleanup.print_table(
        table_title="Deleted Snapshots",
        headers=[
            "resource_group",
            "name",
            "location",
            "created_date",
            "ttl_tag_value",
            "action",
        ],
        object_list=deleted_snapshots,
    )
