import typer
from typing import Optional, List
from .config import settings
# from rich.table import Table
# from rich.console import Console


cli = typer.Typer(help="Azure Disk Snapshot Cleanup", no_args_is_help=True)
# console = Console()


@cli.command("list-sub")
def list_subscription():
    """List all subscriptions that user has access."""
    typer.echo("List all subscriptions that user has access.")


@cli.command("list-rg")
def list_resource_groups(
    subscription_id: Optional[List[str]] = typer.Option(
        default=None, help="List of subscription ID to filter"
    )
):
    """List all resource groups, can be filtered by subscription."""
    typer.echo("List all resource groups, can be filtered by subscription.")


@cli.command("list-snap")
def list_snapshots(
    subscription_id: Optional[List[str]] = typer.Option(
        default=None, help="List of subscription ID to filter"
    ),
    rg_name: Optional[List[str]] = typer.Option(
        default=None, help="List of resource group name to filter"
    )
):
    """List all snapshots, can be filtered by subscriptions and resource groups."""
    typer.echo(
        "List all snapshots, can be filtered by subscriptions and resource groups."
    )


@cli.command("add-snap-tag")
def add_snap_tag(
    subscription_id: Optional[List[str]] = typer.Option(
        default=None, help="List of subscription ID to filter"
    ),
    rg_name: Optional[List[str]] = typer.Option(
        default=None, help="List of resource group name to filter"
    ),
    snap_name: Optional[List[str]] = typer.Option(
        default=None, help="List of snapshot name to filter"
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
    """
    Add time-to-live tag on snapshots that do not already have.
    This action can be filtered by subscriptions, resource groups and snapshots.
    """
    typer.echo("Add time-to-live tag on snapshots that do not already have.")


@cli.command("delete-snap")
def delete_snap_tag(
    subscription_id: Optional[List[str]] = typer.Option(
        default=None, help="List of subscription ID to filter"
    ),
    rg_name: Optional[List[str]] = typer.Option(
        default=None, help="List of resource group name to filter"
    ),
    snap_name: Optional[List[str]] = typer.Option(
        default=None, help="List of snapshot name to filter"
    ),
    dry_run: Optional[bool] = typer.Option(
        default=False, help="Command simulation"
    ),
):
    """
    Delete all Add time-to-live tag on snapshots that do not already have.
    This action can be filtered by subscriptions, resource groups and snapshots.
    """
    typer.echo(
        "Delete all Add time-to-live tag on snapshots that do not already have."
    )
