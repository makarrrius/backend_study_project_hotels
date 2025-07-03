from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env") # есть параметр extra = ingnore, чтобы в env файле брались только те переменные, которые указываются в коде

settings = Settings()