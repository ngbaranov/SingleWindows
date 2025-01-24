from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.models import User, Violations
from app.models.sql_enums import Departments, TypeViolation

router = APIRouter(prefix="/keyword_search", tags=["keyword_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], keyword: str = Query(...)):
    """
    Поиск по ключевым словам
    :param request:
    :param db:
    :param keyword:
    :return:
    """
    stmt = select(User).join(Violations).where(Violations.description.ilike(f"%{keyword}%")).options(joinedload(User.violations))

    result = await db.execute(stmt)
    users = result.unique().scalars().all()
    print(users)
    return templates.TemplateResponse("get_search.html", {"request": request, "users": users})