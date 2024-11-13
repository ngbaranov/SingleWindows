from app.dao.base import BaseDAO
from app.models.models import User, Violations


class UsersDAO(BaseDAO):
    model = User


class ViolationsDAO(BaseDAO):
    model = Violations