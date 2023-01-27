from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
