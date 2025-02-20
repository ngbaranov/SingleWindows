from app.dao.base import BaseDAO
from app.models.models import User, Violations, DepartmentUser, UploadedFile
from auth.model import Admin

class UsersDAO(BaseDAO):
    model = User


class ViolationsDAO(BaseDAO):
    model = Violations


class DepartmentUsersDAO(BaseDAO):
    model = DepartmentUser


class UploadedFilesDAO(BaseDAO):
    model = UploadedFile


class AdminDAO(BaseDAO):
    model = Admin

