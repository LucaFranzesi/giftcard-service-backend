
import os
from dotenv import load_dotenv

from configurations.local import LocalConfig
from configurations.development import DevelopmentConfig
from configurations.production import ProductionConfig

def get_config():
    load_dotenv("../.env")
    env = os.getenv("APP_ENV", "production").lower()  # Default a 'development'

    if env == "production":
        return ProductionConfig()
    elif env == "local":
        return LocalConfig()
    elif env == "development":
        return DevelopmentConfig()
    else:
        raise ValueError(f"Unknown environment: {env}")
    
config = get_config()