from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

engine = create_engine(
    'postgresql+psycopg2://postgres:FinnikSQL@localhost:5432/web_second_life',
)
db_session = scoped_session(sessionmaker(bind=engine))


class Base(DeclarativeBase):
    pass
