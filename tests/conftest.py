import pytest
from datetime import date, datetime, timedelta, time, timezone
from snapcleanup.config import settings
from snapcleanup.azure.cli import *
from snapcleanup.azure.azure import *
from snapcleanup.azure.subscription import *
from snapcleanup.azure.resource_group import *
from snapcleanup.azure.snapshot import *


def mock_list_subscriptions() -> list[SubscriptionInfo]:
    list_subscriptions: list[SubscriptionInfo] = []
    list_subscriptions.append(SubscriptionInfo(
        subscription_id="00000000-0000-0000-0000-000000000000",
        name="Subscription Test"
    ))
    return list_subscriptions


def mock_get_subscription() -> SubscriptionInfo:
    return mock_list_subscriptions()[0]


def mock_list_resource_groups() -> list[ResourceGroupInfo]:
    list_resource_groups: list[ResourceGroupInfo] = []
    list_resource_groups.append(ResourceGroupInfo(name="rg-test", location="brazil-south"))
    return list_resource_groups


def mock_get_resource_group() -> ResourceGroupInfo:
    return mock_list_resource_groups()[0]


def mock_list_snapshots() -> list[SnapshotInfo]:
    creation_date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    ttl_format_date = "%Y-%m-%d"

    creation_date = datetime.now(tz=timezone.utc).strftime(creation_date_format)

    ttl_expired_date = datetime.combine(date.today() - timedelta(days=1), time.min).strftime(ttl_format_date)
    ttl_current_date = datetime.now().strftime(ttl_format_date)
    ttl_future_date = datetime.combine(date.today() + timedelta(days=settings.TTL.DAYS_BY_DEFAULT), time.min).strftime(ttl_format_date)

    list_snapshots: list[SnapshotInfo] = []
    list_snapshots.append(SnapshotInfo(
        resource_group="mock-rg-0",
        snapshot_id="/resourceGroups/mock-rg-0/mock-snap-0",
        name="mock-snap-0",
        location="westus",
        created_date=creation_date,
        tags={}
    ))
    list_snapshots.append(SnapshotInfo(
        resource_group="mock-rg-0",
        snapshot_id="/resourceGroups/mock-rg-0/mock-snap-1",
        name="mock-snap-1",
        location="westus",
        created_date=creation_date,
        tags={settings.TTL.TAG_NAME: ttl_expired_date}
    ))
    list_snapshots.append(SnapshotInfo(
        resource_group="mock-rg-1",
        snapshot_id="/resourceGroups/mock-rg-1/mock-snap-2",
        name="mock-snap-2",
        location="eastus",
        created_date=creation_date,
        tags={settings.TTL.TAG_NAME: ttl_current_date}
    ))
    list_snapshots.append(SnapshotInfo(
        resource_group="mock-rg-1",
        snapshot_id="/resourceGroups/mock-rg-1/mock-snap-3",
        name="mock-snap-3",
        location="eastus",
        created_date=creation_date,
        tags={settings.TTL.TAG_NAME: ttl_future_date}
    ))
    return list_snapshots


def mock_get_snapshot() -> SnapshotInfo:
    return mock_list_snapshots()[0]


@pytest.fixture
def fixture_mock_azure_service(mocker):
    mocker.patch("snapcleanup.azure.azure.AzureService.config_only_show_errors", return_value=True)
    mocker.patch("snapcleanup.azure.azure.AzureService.login", return_value=True)
    

@pytest.fixture
def fixture_mock_subscription_service(mocker):
    mocker.patch("snapcleanup.azure.subscription.SubscriptionService.list_subscriptions", return_value=mock_list_subscriptions())
    mocker.patch("snapcleanup.azure.subscription.SubscriptionService.get_subscription", return_value=mock_get_subscription())
    mocker.patch("snapcleanup.azure.subscription.SubscriptionService.set_subscription", return_value=True)
    

@pytest.fixture
def fixture_mock_resource_group_service(mocker):
    mocker.patch("snapcleanup.azure.resource_group.ResourceGroupService.list_resource_groups", return_value=mock_list_resource_groups())
    mocker.patch("snapcleanup.azure.resource_group.ResourceGroupService.get_resource_group_by_name", return_value=mock_get_resource_group())
    

@pytest.fixture
def fixture_mock_snapshot_service(mocker):
    mocker.patch("snapcleanup.azure.snapshot.SnapshotService.list_snapshots", return_value=mock_list_snapshots())
    mocker.patch("snapcleanup.azure.snapshot.SnapshotService.get_snapshot", return_value=mock_get_snapshot())
    mocker.patch("snapcleanup.azure.snapshot.SnapshotService.update_snapshot_tags", return_value=True)
    mocker.patch("snapcleanup.azure.snapshot.SnapshotService.delete_snapshot", return_value=True)
