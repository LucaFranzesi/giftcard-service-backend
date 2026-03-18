
class BaseConfig:
    APP_NAME: str = "GiftCard Service"
    DEBUG: bool = False
    DATABASE_URI: str = "sqlite:///app.db"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
