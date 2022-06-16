import os
from dynaconf import Dynaconf, Validator


settings = Dynaconf(
    envvar_prefix="SNAPCLEANUP",
    root_path=os.path.dirname(__file__),
    settings_files=["settings.toml"],
)
# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

settings.validators.register(
    Validator("AZURE_SUBSCRIPTION_IDS", must_exist=True),
)

settings.validators.validate()
