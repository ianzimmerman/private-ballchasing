from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from config import DATABASE_LOCATION

engine = create_engine(
    f"sqlite+pysqlite:///{DATABASE_LOCATION}",
    echo=False,
    future=True
)
session = Session(engine)