from sqlalchemy import select, func
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.dao.base import BaseDAO
from app.models.models import User, Violations, DepartmentUser, UploadedFile
from auth.model import Admin

class UsersDAO(BaseDAO):
    model = User


class ViolationsDAO(BaseDAO):
    model = Violations

    @classmethod
    async def get_all_tags(cls, session: AsyncSession) -> list[str]:
        result = await session.execute(
            select(func.distinct(cls.model.tags)).where(cls.model.tags.isnot(None))
        )
        raw_tags = [row[0] for row in result.fetchall() if row[0]]

        # Распарсим теги и соберем уникальные
        tag_set = set()
        for tag_line in raw_tags:
            tags = [tag.strip() for tag in tag_line.split(",")]
            tag_set.update(tag for tag in tags if tag)  # убираем пустые

        return sorted(tag_set)


class DepartmentUsersDAO(BaseDAO):
    model = DepartmentUser


class UploadedFilesDAO(BaseDAO):
    model = UploadedFile


class AdminDAO(BaseDAO):
    model = Admin

