from configurations.base import BaseConfig

class LocalConfig(BaseConfig):
    DEBUG: bool = True
    DATABASE_URI: str = "sqlite:///local.db"
    SECRET: str = "Test ambiente locale"