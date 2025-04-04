from typing import Annotated
from collections import defaultdict

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UsersDAO
from app.database.db_depends import get_db
from app.models.models import User
from app.models.sql_enums import Departments
from app.servise.get_letters import get_available_letters

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# @router.get("/")
# async def get_index(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
#     users = await UsersDAO.get_users_with_details(db, User.department, User.violations)
#
#     departments = defaultdict(list)
#     for user in users:
#         department_name = str(user.department.name.value) if isinstance(user.department.name,
#                                                                         Departments) else user.department.name
#         departments[department_name].append({"surname": user.surname, "name": user.name, "last_name": user.last_name, "id": user.id})
#
#     return templates.TemplateResponse("index.html", {"request": request, 'users': departments})

@router.get("/")
async def admin_panel(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UsersDAO.get_all_users(db)
    available_letters = await get_available_letters(db)
    violations = {
        "Access_mode": "Пропускной режим",
        "Information_security": "Информационная безопасность",
        "Work_schedule": "Трудовой распорядок",
        "Other": "Другое"
    }
    return templates.TemplateResponse("index.html", {"request": request, "users": users, "violations": violations, "available_letters": available_letters})