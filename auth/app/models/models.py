from datetime import datetime, date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base
from app.models.sql_enums import Departments, TypeViolation


class User(Base):
    surname: Mapped[str | None] # Фамилия
    name: Mapped[str | None] # Имя
    last_name: Mapped[str | None] # Отчество

    hired: Mapped[date | None]
    dismissal: Mapped[date | None]
    department_id: Mapped[int] = mapped_column(ForeignKey('departmentusers.id'))

    violations: Mapped[list['Violations']] = relationship("Violations", back_populates="user",
                                                          cascade="all, delete-orphan")

    department: Mapped['DepartmentUser'] = relationship("DepartmentUser", back_populates="users")

    files: Mapped[list['UploadedFile']] = relationship("UploadedFile", back_populates="user_file", cascade="all, delete-orphan")

class Violations(Base):
    type_violation: Mapped[TypeViolation | None] = mapped_column(default=TypeViolation.Access_mode)
    date_violation: Mapped[datetime | None]
    description: Mapped[str | None]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship("User", back_populates="violations")


class DepartmentUser(Base):
    name: Mapped[Departments] = mapped_column(default=Departments.General)

    users: Mapped[list['User']] = relationship("User", back_populates="department")


class UploadedFile(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str]
    filepath: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user_file: Mapped['User'] = relationship("User", back_populates="files")


