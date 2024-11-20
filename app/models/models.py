from datetime import datetime, date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from app.models.sql_enums import Departments, TypeViolation


class User(Base):
    username:Mapped[str]
    address:Mapped[str]
    phone_number:Mapped[str|None]
    hired:Mapped[date]
    dismissal:Mapped[date|None]
    department_id:Mapped[int] = mapped_column(ForeignKey('departmentusers.id'))

    violations:Mapped[list['Violations']] = relationship("Violations",back_populates="user", cascade="all, delete-orphan")

    department:Mapped['DepartmentUser'] = relationship("DepartmentUser",back_populates="users")

class Violations(Base):
    type_violation:Mapped[TypeViolation|None] = mapped_column(default=TypeViolation.Access_mode)
    date_violation:Mapped[datetime|None]
    description:Mapped[str|None]
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))

    user:Mapped['User'] = relationship("User",back_populates="violations")


class DepartmentUser(Base):
    name:Mapped[Departments] = mapped_column(default=Departments.General)

    users:Mapped[list['User']] = relationship("User",back_populates="department")





    
