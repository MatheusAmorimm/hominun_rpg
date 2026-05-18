from typing import Any, Callable

MigrationFn = Callable[[dict[str, Any]], dict[str, Any]]

CURRENT_SAVE_VERSION: int = 1

VERSION_MIGRATIONS: dict[int, MigrationFn] = {
    # 1: migrate_v1_to_v2,
}


def migrate(save_data: dict[str, Any], from_version: int) -> dict[str, Any]:
    version = from_version
    while version < CURRENT_SAVE_VERSION:
        migrate_fn = VERSION_MIGRATIONS.get(version)
        if migrate_fn is None:
            raise ValueError(f"No migration found from version {version}")
        save_data = migrate_fn(save_data)
        version += 1
    return save_data
