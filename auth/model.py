from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped
from app.database.db import (Base)


class Admin(Base):

    username: Mapped[str] = Column(String, unique=True, index=True)
    password: Mapped[str] = Column(String)
    is_admin: Mapped[bool] = Column(Boolean, default=True)