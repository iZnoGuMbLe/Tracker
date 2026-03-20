from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    DEBUG: bool
    GRAFANA_USER: str
    GRAFANA_PASSWORD: str
    GRAFANA_ROOT_URL: str
    REFRESH_TOKEN_EXPIRE_DAYS: int
    VERIFICATION_TOKEN_EXPIRE_HRS: int
    AMQP_URL: str

    class Config:
        env_file = '.env'


settings = Settings()