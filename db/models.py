from typing import List, Optional
from sqlalchemy import ForeignKey, String, create_engine, Integer, Date, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("sqlite+pysqlite:///testevs.db", echo=True)


class Base(DeclarativeBase):
    pass

# class User(Base):
#     __tablename__ = "users_table"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     username: Mapped[int] 
#     registerDate: Mapped[Date]
#     premiumBool: Mapped[bool] = mapped_column(default=False)

#     def __repr__(self) -> str:
#         return f"User(id={self.id}, name={self.username}, regDate={self.registerDate}), premium={self.premiumBool}"

# class selectedCateg(Base):
#     __tablename__ = "user_categ"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     username: Mapped[int] = mapped_column(Integer(50), nullable=False)
#     category: Mapped[String]
    
#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.username!r}, category={self.category!r})"
    
# class selectedCountry(Base):
#     __tablename__ = "user_country"
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     username: Mapped[int] = mapped_column(Integer(50), nullable=False)
#     country: Mapped[String]

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.username!r}, Country={self.category!r})"