from typing import List, Optional
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, sessionmaker

<<<<<<< HEAD
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

# 
=======
engine = create_engine("sqlite+pysqlite:///testevs.db", echo=True)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users_table"
    
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"
>>>>>>> d3d7a51acef3d56b454fbd9b0badb608a7285032
