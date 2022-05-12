from snapcleanup.azure.cli import AzureCli
from snapcleanup.entities import ResourceGroupInfo


class ResourceGroupService:

    @staticmethod
    def list_resource_groups() -> list[ResourceGroupInfo]:
        cmd = ['group', 'list']
        resource_groups = AzureCli.run_cmd(cmd)

        list_resource_groups: list[ResourceGroupInfo] = []
        if isinstance(resource_groups, list) and len(resource_groups) > 0:
            for resource_group in resource_groups:
                list_resource_groups.append(
                    ResourceGroupInfo (
                        name=resource_group.get('name'),
                        location=resource_group.get('location')
                    )
                )
        
        return list_resource_groups


    @staticmethod
    def get_resource_group_by_name(rg_name: str) -> ResourceGroupInfo | None:
        cmd = ['group', 'show', '--name', rg_name]
        resource_group = AzureCli.run_cmd(cmd)
        
        if resource_group:
            return ResourceGroupInfo (
                name=resource_group.get('name'),
                location=resource_group.get('location')
            )
        
        return None
