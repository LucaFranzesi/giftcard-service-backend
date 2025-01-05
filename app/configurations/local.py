from configurations.base import BaseConfig

class LocalConfig(BaseConfig):
    DEBUG: bool = True
    DATABASE_URI: str = "postgresql+psycopg2://postgres:Password%401@localhost/gift-cards-service"
    BCRYPT_SECRET_KEY = '197b2c37c391bed93fe80344fe73b806947a65e36206e05a1a23c2fa12702fe3'
    BCRYPT_ALGORITHM = 'HS256'