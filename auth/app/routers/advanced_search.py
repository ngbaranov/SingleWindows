from typing import Annotated
from collections import Counter

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.models import User, Violations
from app.models.sql_enums import Departments, TypeViolation

router = APIRouter(prefix="/advanced_search", tags=["get_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    violations = {
    "Access_mode": "Пропускной режим",
    "Information_security": "Информационная безопасность",
    "Work_schedule": "Трудовой распорядок",
    "Other": "Другое"
}
    
    return templates.TemplateResponse("advanced_search.html", {"request": request, "violations": violations})




@router.get("/{type_violation}")
async def get_search(request: Request, type_violation: str, db: Annotated[AsyncSession, Depends(get_db)]):
    smtp = select(User).join(Violations).where(Violations.type_violation == type_violation)
    result = await db.execute(smtp)
    users = result.scalars().all()
    violation_users = []
    for user in users:
        violation_users.extend([user.surname, user.name, user.last_name])

    violation_users = Counter(violation_users)
    print(violation_users)


    violations = {
        "Access_mode": "Пропускной режим",
        "Information_security": "Информационная безопасность",
        "Work_schedule": "Трудовой распорядок",
        "Other": "Другое"
    }

    violation = violations.get(type_violation)


    return templates.TemplateResponse("get_advanced_search.html", {"request": request, "users": users, "violation": violation, "violation_users": violation_users})


