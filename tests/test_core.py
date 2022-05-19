from pytest import mark
from snapcleanup.core import DiskSnapshotCleanup
from snapcleanup.entities import ActionStates, ResourceGroupInfo, SnapshotInfo, SubscriptionInfo
from snapcleanup.config import settings


def test_when_set_subscription_then_return_true(fixture_mock_azure_service, fixture_mock_subscription_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    
    # Act
    result = snapcleanup.set_subscription('any')
    
    # Assert
    assert result is True
    print(result)


def test_when_list_subscriptions_then_return_list_of_subscription_info(fixture_mock_azure_service, fixture_mock_subscription_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    
    # Act
    subscriptions = snapcleanup.list_subscriptions()
    
    # Assert
    assert isinstance(subscriptions, list)
    for subscription in subscriptions:
        assert isinstance(subscription, SubscriptionInfo)


def test_when_get_subscription_then_return_subscription_info(fixture_mock_azure_service, fixture_mock_subscription_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    
    # Act
    subscription = snapcleanup.get_subscription('any')
    
    # Assert
    assert isinstance(subscription, SubscriptionInfo)


def test_when_list_resource_groups_then_return_list_of_resource_group_info(fixture_mock_azure_service, fixture_mock_resource_group_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    
    # Act
    resource_groups = snapcleanup.list_resource_groups()
    
    # Assert
    assert isinstance(resource_groups, list)
    for resource_group in resource_groups:
        assert isinstance(resource_group, ResourceGroupInfo)


def test_when_list_snapshots_then_return_list_of_snapshot_info(fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    
    # Act
    snapshots = snapcleanup.list_snapshots()
    
    # Assert
    assert isinstance(snapshots, list)
    for snapshot in snapshots:
        assert isinstance(snapshot, SnapshotInfo)


def test_when_update_snapshot_tag_then_return_list_of_snapshot_info(fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    updated_snapshots = snapcleanup.update_snapshot_tag(
        list_snapshots=snapshots,
        ttl_tag_name=settings.TTL.TAG_NAME,
        ttl_days=settings.TTL.DAYS_BY_DEFAULT,
        dry_run=False
    )
    
    # Assert
    assert isinstance(snapshots, list)
    for snapshot in updated_snapshots:
        assert isinstance(snapshot, SnapshotInfo)


@mark.parametrize("input_snap, expected_action", [
    ("mock-snap-0", ActionStates.PENDING_UPDATE),
    ("mock-snap-1", ActionStates.UPDATED),
    ("mock-snap-2", ActionStates.UPDATED),
    ("mock-snap-3", ActionStates.UPDATED),
])
def test_when_dry_run_update_snapshot_tag_then_return_list_with_one_snapshot_pending_update_and_others_updated(input_snap, expected_action, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    updated_snapshots = snapcleanup.update_snapshot_tag(
        list_snapshots=snapshots,
        ttl_tag_name=settings.TTL.TAG_NAME,
        ttl_days=settings.TTL.DAYS_BY_DEFAULT,
        dry_run=True
    )
    
    # Assert
    for snapshot in updated_snapshots:
        if snapshot.name == input_snap:
            assert snapshot.action == expected_action


@mark.parametrize("input_snap, expected_action", [
    ("mock-snap-0", ActionStates.UPDATED),
    ("mock-snap-1", ActionStates.UPDATED),
    ("mock-snap-2", ActionStates.UPDATED),
    ("mock-snap-3", ActionStates.UPDATED),
])
def test_when_update_snapshot_tag_then_return_list_with_snapshots_updated(input_snap, expected_action, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    updated_snapshots = snapcleanup.update_snapshot_tag(
        list_snapshots=snapshots,
        ttl_tag_name=settings.TTL.TAG_NAME,
        ttl_days=settings.TTL.DAYS_BY_DEFAULT,
        dry_run=False
    )
    
    # Assert
    for snapshot in updated_snapshots:
        if snapshot.name == input_snap:
            assert snapshot.action == expected_action


def test_when_delete_snapshots_then_return_list_of_snapshot_info(fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    deleted_snapshots = snapcleanup.delete_snapshots(
        list_snapshots=snapshots,
        dry_run=False
    )
    
    # Assert
    assert isinstance(snapshots, list)
    for snapshot in deleted_snapshots:
        assert isinstance(snapshot, SnapshotInfo)


@mark.parametrize("input_snap, expected_action", [
    ("mock-snap-0", ActionStates.NOT_DEFINED),
    ("mock-snap-1", ActionStates.PENDING_DELETE),
    ("mock-snap-2", ActionStates.NOT_DEFINED),
    ("mock-snap-3", ActionStates.NOT_DEFINED),
])
def test_when_dry_run_delete_snapshots_then_return_list_with_one_snapshot_pending_delete_and_others_not_defined(input_snap, expected_action, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    deleted_snapshots = snapcleanup.delete_snapshots(
        list_snapshots=snapshots,
        dry_run=True
    )
    
    # Assert
    for snapshot in deleted_snapshots:
        if snapshot.name == input_snap:
            assert snapshot.action == expected_action


@mark.parametrize("input_snap, expected_action", [
    ("mock-snap-0", ActionStates.NOT_DEFINED),
    ("mock-snap-1", ActionStates.DELETED),
    ("mock-snap-2", ActionStates.NOT_DEFINED),
    ("mock-snap-3", ActionStates.NOT_DEFINED),
])
def test_when_update_snapshot_tag_then_return_list_with_snapshots_updated(input_snap, expected_action, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    snapcleanup = DiskSnapshotCleanup(client_id="any", client_secret="any", tenant_id="any")
    snapshots = snapcleanup.list_snapshots()
    
    # Act
    deleted_snapshots = snapcleanup.delete_snapshots(
        list_snapshots=snapshots,
        dry_run=False
    )
    
    # Assert
    for snapshot in deleted_snapshots:
        if snapshot.name == input_snap:
            assert snapshot.action == expected_action
