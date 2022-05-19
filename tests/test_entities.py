import re
import sys
from io import StringIO
from snapcleanup.entities import ActionStates, SnapshotInfo


def create_snapshot_object():
    return SnapshotInfo(
        resource_group="rg-test",
        snapshot_id="/rg-test/snap-test",
        name="snap-test",
        location="eastus",
        created_date="2022-12-30T12:30:50.123456-0300",
    )


def test_when_action_states_is_printed_on_stdout_then_display_enum_value():
    # Arrange
    action = ActionStates.NOT_DEFINED
    expected_value = "Not Defined"
    captured_output = StringIO()
    sys.stdout = captured_output
    
    # Act
    print(action)
    sys.stdout = sys.__stdout__
    
    # Assert
    assert expected_value in captured_output.getvalue()


def test_when_create_snapshot_info_without_tags_then_create_empty_dict_tags():
    # Arrange
    snapshot = create_snapshot_object()
    
    # Assert
    assert snapshot.tags == {}


def test_when_create_snapshot_info_then_return_formated_created_date():
    # Arrange
    snapshot = create_snapshot_object()

    # Assert
    assert re.match("[0-9]{4}(-[0-9]{2}){2} ([0-9]{2}:){2}[0-9]{2}", snapshot.created_date)
