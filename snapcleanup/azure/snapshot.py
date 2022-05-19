from snapcleanup.azure.cli import AzureCli
from snapcleanup.entities import SnapshotInfo


class SnapshotService:
    @staticmethod
    def list_snapshots() -> list[SnapshotInfo]:
        cmd = ["snapshot", "list"]
        snapshots = AzureCli.run_cmd(cmd)

        list_snapshots: list[SnapshotInfo] = []
        if isinstance(snapshots, list) and len(snapshots) > 0:
            for snapshot in snapshots:
                list_snapshots.append(
                    SnapshotInfo(
                        resource_group=snapshot.get("resourceGroup"),
                        snapshot_id=snapshot.get("id"),
                        name=snapshot.get("name"),
                        location=snapshot.get("location"),
                        created_date=snapshot.get("timeCreated"),
                        tags=snapshot.get("tags"),
                    )
                )

        return list_snapshots

    @staticmethod
    def get_snapshot(snapshot_name: str, resource_group_name: str) -> SnapshotInfo | None:
        cmd = [
            "snapshot",
            "show",
            "--name",
            snapshot_name,
            "--resource-group",
            resource_group_name,
        ]
        snapshot = AzureCli.run_cmd(cmd)

        if snapshot:
            return SnapshotInfo(
                resource_group=snapshot.get("resourceGroup"),
                snapshot_id=snapshot.get("id"),
                name=snapshot.get("name"),
                location=snapshot.get("location"),
                created_date=snapshot.get("timeCreated"),
                tags=snapshot.get("tags"),
            )

        return None

    @staticmethod
    def update_snapshot_tags(list_snapshot_id: list[str], tags: dict) -> bool:
        if len(list_snapshot_id) > 0:
            cmd = ["snapshot", "update", "--ids"]
            for snapshot_id in list_snapshot_id:
                cmd.append(snapshot_id)

            cmd.append("--set")
            for key, value in tags.items():
                cmd.append(f"tags.{key}={value}")

            result = AzureCli.run_cmd(cmd)
            if result:
                return True
        return False

    @staticmethod
    def delete_snapshot(list_snapshot_id: list[str]) -> bool:
        if len(list_snapshot_id) > 0:
            cmd = ["snapshot", "delete", "--ids"]
            for snapshot_id in list_snapshot_id:
                cmd.append(snapshot_id)

            result = AzureCli.run_cmd(cmd)
            if result:
                return True
        return False
