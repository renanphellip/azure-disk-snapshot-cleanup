from azure.cli.core import get_default_cli


class AzureCli:
    @staticmethod
    def run_cmd(args: list[str], output="none"):

        cli = get_default_cli()
        args.append("-o")
        args.append(output)

        cli.invoke(args)
        if cli.result.result:
            return cli.result.result
        if cli.result.error:
            raise cli.result.error
        return True
