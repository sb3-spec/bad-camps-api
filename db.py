from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"postgresql+psycopg2://postgres:TWAYdEGQUdSF4K6yBUlZ@containers-us-west-102.railway.app:6609/railway"

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:TWAYdEGQUdSF4K6yBUlZ@containers-us-west-102.railway.app:6609/railway"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()