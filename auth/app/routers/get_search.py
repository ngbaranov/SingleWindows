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


router = APIRouter(prefix="/get_search", tags=["get_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], query: str = Query(...)):

    stmt = select(User).where(or_(User.surname.ilike(f"%{query}%"),
                                  User.name.ilike(f"%{query}%"),
                                  User.last_name.ilike(f"%{query}%")))


    result = await db.execute(stmt)
    users = result.scalars().all()
    print(users)
    return templates.TemplateResponse("get_search.html", {"request": request, "users": users})



