import sys
import os
import json
from io import StringIO
from rich.console import Console
from snapcleanup.entities import ResourceGroupInfo
from snapcleanup.output import Output


def create_resource_group_list() -> list[ResourceGroupInfo]:
    resource_groups: list[ResourceGroupInfo] = []
    resource_groups.append(
        ResourceGroupInfo(name=f"rg-test", location="brazil-south"),
    )
    return resource_groups


def test_when_print_table_is_printed_then_display_table_data():
    # Arrange
    output = Output()
    console = Console()
    captured_output = StringIO()
    sys.stdout = captured_output
    list_resource_groups = create_resource_group_list()
    expected_data = "brazil-south"

    # Act
    table = output.print_table(
        table_title="List Resource Groups",
        headers=["name", "location"],
        object_list=list_resource_groups,
    )
    console.print(table)
    sys.stdout = sys.__stdout__

    # Assert
    assert expected_data in captured_output.getvalue()


def test_when_created_csv_file_then_file_must_exists(request):
    # Arrange
    output = Output()
    list_resource_groups = create_resource_group_list()
    fields = ["name", "location"]
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("resource_groups.csv")

    # Act
    try:
        output.create_csv_file(
            file_path=file_path, headers=fields, object_list=list_resource_groups
        )

        # Assert
        assert os.path.exists(file_path) == True
    finally:
        os.remove(file_path)


def test_when_created_csv_file_then_data_has_valid_csv_format(request):
    # Arrange
    output = Output()
    list_resource_groups = create_resource_group_list()
    fields = ["name", "location"]
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("resource_groups.csv")
    expected_content = "name;location\nrg-test;brazil-south"

    # Act
    output.create_csv_file(file_path=file_path, headers=fields, object_list=list_resource_groups)
    csv_file = open(file=file_path, mode="r", encoding="utf-8")
    csv_content = csv_file.read()
    csv_file.close()
    os.remove(file_path)

    # Assert
    assert expected_content in csv_content


def test_when_created_json_file_then_data_has_valid_json_format(request):
    # Arrange
    output = Output()
    list_resource_groups = create_resource_group_list()
    fields = ["name", "location"]
    tmpdir = request.getfixturevalue("tmpdir")
    file_path = tmpdir.join("resource_groups.csv")
    expected_content = [{"location": "brazil-south", "name": "rg-test"}]
    expected_json_string = json.dumps(expected_content).replace('"', "'")

    # Act
    output.create_json_file(file_path=file_path, headers=fields, object_list=list_resource_groups)
    json_file = open(file=file_path, mode="r", encoding="utf-8")
    json_content = str(json.loads(json_file.read()))
    json_file.close()
    os.remove(file_path)

    # Assert
    assert expected_json_string in json_content
