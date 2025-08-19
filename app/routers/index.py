from typing import Annotated
from collections import defaultdict

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UsersDAO, ViolationsDAO
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

from collections import defaultdict
import re

@router.get("/")
async def admin_panel(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UsersDAO.get_users_with_details(db, User.violations)

    user_data = []
    tags_map = defaultdict(list)

    for user in users:
        full_user = {
            "id": user.id,
            "surname": user.surname,
            "name": user.name,
            "last_name": user.last_name,
        }
        user_data.append(full_user)

        for violation in user.violations:
            if violation.tags:
                for tag in map(str.strip, violation.tags.split(",")):
                    if tag:
                        tags_map[tag].append(full_user)

    available_letters = await get_available_letters(db)
    violations = {
        "Access_mode": "Пропускной режим",
        "Information_security": "Информационная безопасность",
        "Work_schedule": "Трудовой распорядок",
        "Other": "Другое"
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": user_data,
        "violations": violations,
        "tags": sorted(tags_map.keys()),
        "available_letters": available_letters,
        "users_by_tag": tags_map  # 👈 Новый ключ
    })

