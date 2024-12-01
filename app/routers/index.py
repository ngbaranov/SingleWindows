from typing import Annotated
from collections import defaultdict

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UsersDAO
from app.database.db_depends import get_db
from app.models.sql_enums import Departments

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_index(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UsersDAO.get_users_with_details(db)

    departments = defaultdict(list)
    for user in users:
        department_name = str(user.department.name.value) if isinstance(user.department.name,
                                                                        Departments) else user.department.name
        departments[department_name].append({"name": user.username, "id": user.id})

    return templates.TemplateResponse("index.html", {"request": request, 'users': departments})
