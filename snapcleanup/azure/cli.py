from azure.cli.core import get_default_cli
from rich.console import Console


class AzureCli:
    @staticmethod
    def run_cmd(args: list[str], output="none"):
        console = Console()
        
        cli = get_default_cli()
        args.append("-o")
        args.append(output)
        
        cli.invoke(args)
        if cli.result.result:
            return cli.result.result
        if cli.result.error:
            console.print(
                f'Exception: {cli.result.error}',
                style='red'
            )
            exit(1)
        return True
