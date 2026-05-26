import os

from dotenv import load_dotenv

_ = load_dotenv()


class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "arahku")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    MODEL_API_URL: str = os.getenv("MODEL_API_URL", "http://127.0.0.1:9000")


settings = Settings()
