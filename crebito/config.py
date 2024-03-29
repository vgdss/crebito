"""Settings module"""
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="crebito",
    settings_files=['settings.toml', '.secrets.toml'],
    load_dotenv=False,
)