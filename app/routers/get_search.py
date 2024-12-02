from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.models import User
from app.models.sql_enums import Departments, TypeViolation


router = APIRouter(prefix="/get_search", tags=["get_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], query: str = Query()):
    results = select(User).where(User.username.ilike(f"%{query}%"))  # (await UsersDAO.get_users_by_query(query))
    users = await db.execute(results)
    users = users.scalars().all()

    # query = select(cls.model).where(cls.model.id == user_id).options(joinedload(cls.model.department),
    #                                                                  joinedload(cls.model.violations))
    # result = await session.execute(query)
    return templates.TemplateResponse("get_search.html", {"request": request, "users": users})