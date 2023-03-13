from sqlalchemy import Column
from sqlalchemy.types import Integer, Float, String
from sqlalchemy.orm import declarative_base 

Base = declarative_base()

class Dato(Base):
    __tablename__ = 'dato'
    id = Column(String(255), primary_key=True)
    CODDISA = Column(String(25)) 
    NOMDISA = Column(String(25)) 
    CODIGO_PRE = Column(String(25)) 
    ESTABLEC = Column(String(25)) 
    SOBRESTOCK = Column(Integer()) 
    NORMOSTOCK = Column(Integer()) 
    SUBSTOCK = Column(Integer()) 
    DESABATECIDO = Column(Integer()) 
    TOTAL = Column(Integer())  
    DESABATECIDOX = Column(Float()) 
    SUBSTOCKX = Column(Float()) 
    DISPO = Column(Float()) 
