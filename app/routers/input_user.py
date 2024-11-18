from datetime import datetime, date

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.sql_enums import Departments, TypeViolation

from typing import Annotated

router = APIRouter(prefix="/input_user", tags=["input_user"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_input_user(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UsersDAO.get_all_users(db)
    return templates.TemplateResponse("input_user.html", {"request": request, "users": users})


@router.post("/get_input_user")
async def post_input_user(request: Request,
                          db: Annotated[AsyncSession, Depends(get_db)],
                          username: str = Form(),
                          address: str = Form(),
                          phone_number: str = Form(),
                          department: str = Form(),
                          hired: str = Form(),
                          dismissal: str | None = Form(),
                          type_violation: str | None = Form(),
                          date_violation: str | None = Form(),
                          description: str | None = Form(),
                          ):
    hired_date = datetime.strptime(hired, "%Y-%m-%d").date() if hired else None
    dismissal_date = datetime.strptime(dismissal, "%Y-%m-%d").date() if dismissal else None
    date_violation = datetime.strptime(date_violation, "%Y-%m-%d").date() if date_violation else None

    user = await UsersDAO.add(db, username=username, address=address, phone_number=phone_number,
                       department=department, hired=hired_date, dismissal=dismissal_date)
    violation = await ViolationsDAO.add(db, type_violation=type_violation, date_violation=date_violation,
                        description=description, user_id=user.id)


    departments_dict = {department.name: department.value for department in Departments}
    department = departments_dict.get(department)
    violations_dict = {violation.name: violation.value for violation in TypeViolation}
    type_violation = violations_dict.get(type_violation)

    return templates.TemplateResponse("get_input_user.html", {"request": request, "user": user,
                                                              "department": department, "violation": violation,
                                                              "type_violation": type_violation})

