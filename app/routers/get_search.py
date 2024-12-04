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
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], query: str = Query(...)):

    stmt = select(User).where(User.username.ilike(f"%{query}%"))
    result = await db.execute(stmt)
    users = result.scalars().all()
    return templates.TemplateResponse("get_search.html", {"request": request, "users": users})

