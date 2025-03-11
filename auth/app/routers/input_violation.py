from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.sql_enums import Departments, TypeViolation
from auth.service.current_user import get_current_admin_user

router = APIRouter(prefix="/input_violation", tags=["input_violation"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{id}")
async def get_input_violation(request: Request, id: int, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    user = await UsersDAO.get_user_by_id(db, id)
    return templates.TemplateResponse("input_violation.html", {"request": request, "user": user})


@router.post("/get_input_violation/{id}")
async def input_violation(request: Request, id: int, db: Annotated[AsyncSession, Depends(get_db)],
                          type_violation: str = Form(),
                          date_violation: str = Form(),
                          description: str = Form(),
                          ):
    date_violation = datetime.strptime(date_violation, "%Y-%m-%d").date() if date_violation else None
    await ViolationsDAO.add(db, type_violation=type_violation, date_violation=date_violation,
                            description=description, user_id=id)
    user = await UsersDAO.get_user_by_id(db, id)
    return templates.TemplateResponse("user.html", {"request": request, "user": user})