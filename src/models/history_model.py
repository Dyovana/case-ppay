from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config.config_database import PostgresSettings

credentials = PostgresSettings()
engine = create_engine(
    f"postgresql://{credentials.POSTGRES_USER}:{credentials.POSTGRES_PASSWORD}@"
    f"{credentials.POSTGRES_HOST}:{credentials.POSTGRES_PORT}/{credentials.POSTGRES_DB}",
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)


def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session()
    try:
        yield session
    finally:
        session.close()
