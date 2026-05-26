import os

# from app.core.config import settings
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

_ = load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(
        "mysql://",
        "mysql+pymysql://",
        1,
    )
# DATABASE_URL = (
#     f"mysql+pymysql://{settings.DB_USER}"
#     f":{settings.DB_PASSWORD}"
#     f"@{settings.DB_HOST}"
#     f":{settings.DB_PORT}"
#     f"/{settings.DB_NAME}"
# )

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base modern SQLAlchemy 2.x
class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
