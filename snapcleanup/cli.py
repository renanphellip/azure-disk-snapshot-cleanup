import typer
from typing import Optional, List
from snapcleanup.config import settings
from snapcleanup.core import DiskSnapshotCleanup
from rich.console import Console
from rich.table import Table


cli = typer.Typer(help="Azure Disk Snapshot Cleanup", no_args_is_help=True)
snap_cleanup = DiskSnapshotCleanup(
    client_id=settings.AZURE.AZURE_CLIENT_ID,
    client_secret=settings.AZURE.AZURE_CLIENT_SECRET,
    tenant_id=settings.AZURE.AZURE_TENANT_ID,
    subscription_id=settings.AZURE.AZURE_SUBSCRIPTION_ID
)
console = Console()


@cli.command("list-sub")
def list_subscriptions(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    )
):
    """List all subscriptions that user has access."""
    table = snap_cleanup.list_subscriptions()
    console.print(table)


@cli.command("list-rg")
def list_resource_groups(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    )
):
    """List all resource groups."""
    table = snap_cleanup.list_resource_groups()
    console.print(table)


@cli.command("list-snap")
def list_snapshots(
    csv: Optional[bool] = typer.Option(
        default=False, help="Export output to CSV file"
    ),
    json: Optional[bool] = typer.Option(
        default=False, help="Export output to JSON file"
    )
):
    """List all snapshots."""
    table = snap_cleanup.list_snapshots()
    console.print(table)


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
    )
):
    """Add time-to-live tag on snapshots that do not already have."""
    snapshots = snap_cleanup.list_snapshots()
    table = snap_cleanup.update_snapshot_tag(
        list_snapshots=snapshots,
        ttl_tag_name=ttl_tag_name,
        ttl_days=ttl_days,
        dry_run=dry_run
    )
    console.print(table)


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
    )
):
    """Delete all Add time-to-live tag on snapshots that do not already have."""
    snapshots = snap_cleanup.list_snapshots()
    table = snap_cleanup.delete_snapshots(
        list_snapshots=snapshots,
        dry_run=dry_run
    )
    console.print(table)
