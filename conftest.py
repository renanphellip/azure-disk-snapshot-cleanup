# import pytest
# from datetime import date, datetime, timedelta
# from snapcleanup.config import settings
# from snapcleanup.azure.cli import *
# from snapcleanup.azure.azure import *
# from snapcleanup.azure.subscription import *
# from snapcleanup.azure.resource_group import *
# from snapcleanup.azure.snapshot import *


# def mock_list_subscriptions() -> list[SubscriptionInfo]:
#     list_subscriptions: list[SubscriptionInfo] = []
#     list_subscriptions.append(SubscriptionInfo(
#         subscription_id="00000000-0000-0000-0000-000000000000",
#         name="Subscription 0"
#     ))
#     list_subscriptions.append(SubscriptionInfo(
#         subscription_id="11111111-1111-1111-1111-111111111111",
#         name="Subscription 1"
#     ))
#     return list_subscriptions


# def mock_get_subscription() -> SubscriptionInfo:
#     return mock_list_subscriptions()[0]


# def mock_list_resource_groups() -> list[ResourceGroupInfo]:
#     list_resource_groups: list[ResourceGroupInfo] = []
#     list_resource_groups.append(ResourceGroupInfo(name="mock-rg-0", location="westus"))
#     list_resource_groups.append(ResourceGroupInfo(name="mock-rg-1", location="eastus"))
#     return list_resource_groups


# def mock_get_resource_group() -> ResourceGroupInfo:
#     return mock_list_resource_groups()[0]


# def mock_list_snapshots() -> list[SnapshotInfo]:
#     snapshot_format_date = "%Y-%m-%dT%H:%M:%S.%f"
#     ttl_format_date = "%Y-%m-%d"

#     expired_date = (date.today() - timedelta(days=1))
#     current_date = datetime.now().strftime(snapshot_format_date)
#     future_date = (date.today() + timedelta(days=30)).strftime(snapshot_format_date)

#     list_snapshots: list[SnapshotInfo] = []
#     list_snapshots.append(SnapshotInfo(
#         resource_group="mock-rg-0",
#         snapshot_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mock-rg-0/providers/Microsoft.Compute/snapshots/mock-snap-0",
#         name="mock-snap-0",
#         location="westus",
#         created_date=current_date,
#         tags={}
#     ))
#     list_snapshots.append(SnapshotInfo(
#         resource_group="mock-rg-0",
#         snapshot_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/mock-rg-0/providers/Microsoft.Compute/snapshots/mock-snap-1",
#         name="mock-snap-1",
#         location="westus",
#         created_date=current_date,
#         tags={settings.TTL.TAG_NAME: datetime.strftime(expired_date, ttl_format_date)}
#     ))
#     list_snapshots.append(SnapshotInfo(
#         resource_group="mock-rg-1",
#         snapshot_id="/subscriptions/11111111-1111-1111-1111-111111111111/resourceGroups/mock-rg-1/providers/Microsoft.Compute/snapshots/mock-snap-2",
#         name="mock-snap-2",
#         location="eastus",
#         created_date=current_date,
#         tags={settings.TTL.TAG_NAME: datetime.strftime(current_date, ttl_format_date)}
#     ))
#     list_snapshots.append(SnapshotInfo(
#         resource_group="mock-rg-1",
#         snapshot_id="/subscriptions/11111111-1111-1111-1111-111111111111/resourceGroups/mock-rg-1/providers/Microsoft.Compute/snapshots/mock-snap-3",
#         name="mock-snap-3",
#         location="eastus",
#         created_date=current_date,
#         tags={settings.TTL.TAG_NAME: datetime.strftime(future_date, ttl_format_date)}
#     ))
#     return list_snapshots


# def mock_get_snapshot() -> SnapshotInfo:
#     return mock_list_snapshots()[0]


# @pytest.fixture(autouse=True, scope="function")
# def fixture_mock_cli_calls(mocker):
#     mocker.patch("snapcleanup.azure.cli.AzureCli.run_cmd", return_value=True)
#     mocker.patch("snapcleanup.azure.azure.AzureService.config_only_show_errors", return_value=True)
#     mocker.patch("snapcleanup.azure.azure.AzureService.login", return_value=True)
#     mocker.patch("snapcleanup.azure.subscription.SubscriptionService.list_subscriptions", return_value=mock_list_subscriptions())
#     mocker.patch("snapcleanup.azure.subscription.SubscriptionService.get_subscription", return_value=mock_get_subscription())
#     mocker.patch("snapcleanup.azure.subscription.SubscriptionService.set_subscription", return_value=True)
#     mocker.patch("snapcleanup.azure.resource_group.ResourceGroupService.list_resource_groups", return_value=mock_list_resource_groups())
#     mocker.patch("snapcleanup.azure.resource_group.ResourceGroupService.get_resource_group_by_name", return_value=mock_get_resource_group())
#     mocker.patch("snapcleanup.azure.snapshot.SnapshotService.list_snapshots", return_value=mock_list_snapshots())
#     mocker.patch("snapcleanup.azure.snapshot.SnapshotService.get_snapshot", return_value=mock_get_snapshot())
#     mocker.patch("snapcleanup.azure.snapshot.SnapshotService.update_snapshot_tags", return_value=True)
#     mocker.patch("snapcleanup.azure.snapshot.SnapshotService.delete_snapshot", return_value=True)
