import os
from prettytable import PrettyTable
from rich.console import Console
from rich.table import Table
from prettytable import PrettyTable


class Output:
    def __init__(self):
        self.__console = Console()

    def __create_pretty_table(self, headers: list[str], object_list: list[object]):
        """
        This private method its used only to create a PrettyTable to
        facilitate exporting data to JSON files
        """
        try:
            table = PrettyTable(headers)
            for item in object_list:
                values = [str(getattr(item, header)) for header in headers]
                table.add_row(values)
            return table
        except AttributeError:
            self.__console.print(
                f"The table headers must be equivalent object attributes name.",
                style="red",
            )
            exit(1)
        except Exception as error:
            self.__console.print(error, style="red")
            exit(1)

    def print_table(self, table_title: str, headers: list[str], object_list: list[object]) -> Table:
        try:
            with self.__console.status("Creating table..."):
                table = Table(title=f"[bold]{table_title}[/]")
                for header in headers:
                    table.add_column(header)
                for item in object_list:
                    values = [str(getattr(item, header)) for header in headers]
                    table.add_row(*values)
                self.__console.print("\n", table)
                return table
        except AttributeError:
            self.__console.print(
                f"The table headers must be equivalent object attributes name.",
                style="red",
            )
            exit(1)
        except Exception as error:
            self.__console.print(error, style="red")
            exit(1)

    def create_csv_file(
        self,
        file_path: str,
        headers: list[str],
        object_list: list[object],
        delimiter: str = ";",
        verbose: bool = False,
    ) -> bool:
        try:
            with self.__console.status("Creating CSV file..."):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file=file_path, mode="w", encoding="utf-8") as csv_file:
                    fields = delimiter.join(headers) + "\n"
                    csv_file.write(fields)
                    for item in object_list:
                        values = [str(getattr(item, header)) for header in headers]
                        row_values = delimiter.join(values) + "\n"
                        csv_file.write(row_values)
                self.__console.print(f"{file_path} has been created.", style="green")
        except Exception as error:
            self.__console.print(f"Failed to create: {file_path}", style="red")
            if verbose:
                self.__console.print(f"Exception: {error}", style="red")
            exit(1)

    def create_json_file(
        self,
        file_path: str,
        headers: list[str],
        object_list: list[object],
        indent_spaces: int = 4,
        verbose: bool = False,
    ) -> bool:
        table = self.__create_pretty_table(headers, object_list)
        json_string = table.get_json_string(header=False, indent=indent_spaces)
        try:
            with self.__console.status("Creating JSON file..."):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file=file_path, mode="w", encoding="utf-8") as json_file:
                    json_file.write(json_string)
                self.__console.print(f"{file_path} has been created.", style="green")
        except Exception as error:
            self.__console.print(f"Failed to create: {file_path}", style="red")
            if verbose:
                self.__console.print(f"Exception: {error}", style="red")
            exit(1)
