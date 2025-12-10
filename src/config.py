from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REDIS_URL(self): # адрес для подключения к БД - DSN - формат строки подключения
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @property
    def db_url(self): # адрес для подключения к БД - DSN - формат строки подключения
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=".env") # есть параметр extra = ingnore, чтобы в env файле брались только те переменные, которые указываются в коде

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
settings = Settings()