

from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from app.models.sql_enums import Departments, TypeViolation


class User(Base):
    username:Mapped[str]
    address:Mapped[str]
    phone_number:Mapped[str|None]
    department:Mapped[Departments] = mapped_column(default=Departments.General)
    hired:Mapped[DateTime]
    dismissal:Mapped[DateTime|None]

    violations:Mapped[list['Violations']] = relationship("Violations",back_populates="user", cascade="all, delete-orphan")


class Violations(Base):
    type_violation:Mapped[TypeViolation|None] = mapped_column(default=TypeViolation.Access_mode)
    date_violation:Mapped[DateTime|None]
    description:Mapped[str|None]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    user:Mapped['User'] = relationship("User",back_populates="violations")




    
