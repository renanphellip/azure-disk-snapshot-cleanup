import os
from dynaconf import Dynaconf, Validator


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    root_path=os.path.dirname(__file__),
    settings_files=["settings.toml", ".secrets.toml"],
)
# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

settings.validators.register(
    Validator("AZURE_CLIENT_ID", must_exist=True),
    Validator("AZURE_CLIENT_SECRET", must_exist=True),
    Validator("AZURE_TENANT_ID", must_exist=True),
    Validator("AZURE_SUBSCRIPTION_ID", must_exist=True),
)

settings.validators.validate()
