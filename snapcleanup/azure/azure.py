from snapcleanup.azure.cli import AzureCli


class AzureService:

    @staticmethod
    def login(client_id: str, client_secret: str, tenant_id: str) -> bool:
        cmd = ['login', '--service-principal', '-u', client_id, '-p', client_secret, '--tenant', tenant_id]
        result = AzureCli.run_cmd(cmd)
        if result:
            return True
        return False
