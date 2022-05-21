from typer.testing import CliRunner
from snapcleanup.app import app

runner = CliRunner()

def test_when_invoke_list_sub_command_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_subscription_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("list_subscriptions")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    expected_output = "Subscription Test"
    args = ["list-sub", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_when_invoke_list_rg_command_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_resource_group_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("list_resource_groups")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    expected_output = "rg-test"
    args = ["list-rg", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_when_invoke_list_snap_command_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("list_snapshots")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    expected_output = "mock-snap-2"
    args = ["list-snap", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_when_invoke_update_snap_tag_command_and_dry_run_option_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("updated_snapshots_simulation")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    expected_output = "Pending"
    args = ["update-snap-tag", "--dry-run", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_when_invoke_update_snap_tag_command_option_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("updated_snapshots")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    output = "Pending"
    args = ["update-snap-tag", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert output not in result.stdout


def test_when_invoke_delete_snap_command_and_dry_run_option_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("deleted_snapshots_simulation")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    expected_output = "Pending"
    args = ["delete-snap", "--dry-run", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert expected_output in result.stdout


def test_when_invoke_delete_snap_command_option_then_return_exit_code_zero_and_display_output(request, fixture_mock_azure_service, fixture_mock_snapshot_service):
    # Arrange
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("deleted_snapshots")
    csv_path = file_path.join(".csv")
    json_path = file_path.join(".json")
    output = "Pending"
    args = ["delete-snap", "--csv", csv_path, "--json", json_path]
    
    # Act
    result = runner.invoke(app, args)

    # Assert
    assert result.exit_code == 0
    assert output not in result.stdout
