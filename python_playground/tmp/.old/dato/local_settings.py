from dataclasses import dataclass
from sqlalchemy import create_engine, Column
from sqlalchemy_utils import database_exists, create_database
from pandas import DataFrame
from sqlalchemy.types import Integer, Float, String
from sqlalchemy.orm import declarative_base, Session 
from uuid import uuid4
from time import sleep


Base = declarative_base()

@dataclass(frozen=True)
class Settings:
    pguser = 'dopel'
    pgpasswd = '1234'
    pghost = '192.168.1.18'
    pgport = 3001


def get_engine(user, passwd, host, port, db_name):
    # uri_base = f'postgresql://{user}:{passwd}@{host}:{port}/{db_name}'
    uri_base = f'postgresql://nraxnmwjkbqkbz:e886c75c3afd1a6de316d39ccc0d7c7460773b8659a4b26e640773343d3a2127@ec2-54-161-255-125.compute-1.amazonaws.com:5432/d91nrpfrbi3mtn'
    if not database_exists(uri_base):
        create_database(uri_base)
    engine = create_engine(uri_base, echo=True)
    Base.metadata.create_all(engine)
    current_session = Session(bind=engine)
    return current_session

def parse_db_dump(DataFrame, current_session):
    columns = DataFrame.columns[1:]
    for row in DataFrame.values:
        new_dato = Dato()
        for index, column in enumerate(columns):
            setattr(new_dato, column, row[index + 1])
        new_dato.id = str(uuid4())
        current_session.add(new_dato)
        current_session.commit()


class Dato(Base):
    __tablename__ = 'dato'
    id = Column(String(255), primary_key=True)
    CODDISA = Column(String(255)) 
    NOMDISA = Column(String(255)) 
    CODIGO_PRE = Column(String(255)) 
    ESTABLEC = Column(String(255)) 
    SOBRESTOCK = Column(Integer()) 
    NORMOSTOCK = Column(Integer()) 
    SUBSTOCK = Column(Integer()) 
    DESABASTECIDO = Column(Integer()) 
    TOTAL = Column(Integer())  
    DESABASTECIDOX = Column(Float()) 
    SUBSTOCKX = Column(Float()) 
    DISPO = Column(Float()) 
