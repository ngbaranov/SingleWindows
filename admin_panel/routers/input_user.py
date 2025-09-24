import os
from datetime import datetime

import aiofiles
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO, UploadedFilesDAO
from app.database.db_depends import get_db
from app.models.sql_enums import Departments, TypeViolation
from app.servise.violations_search import embed_one_violation

from typing import Annotated

from auth.service.current_user import get_current_admin_user
router = APIRouter(prefix="/input_user", tags=["input_user"])
templates = Jinja2Templates(directory=["app/templates", "admin_panel/templates"])


@router.get("/")
async def get_input_user(request: Request, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    users = await UsersDAO.get_all_users(db)
    return templates.TemplateResponse("input_user.html", {"request": request, "users": users})


@router.post("/get_input_user")
async def post_input_user(request: Request,
                          db: Annotated[AsyncSession, Depends(get_db)],
                          surname: str = Form(),
                          name: str = Form(),
                          last_name: str = Form(),
                          department: str = Form(),
                          hired: str = Form(),
                          dismissal: str | None = Form(),
                          type_violation: str | None = Form(),
                          date_violation: str | None = Form(),
                          tags: str | None = Form(),
                          description: str | None = Form(),
                          uploaded_files: UploadFile = File(None),
                          ):
    hired_date = datetime.strptime(hired, "%Y-%m-%d").date() if hired else None
    dismissal_date = datetime.strptime(dismissal, "%Y-%m-%d").date() if dismissal else None
    date_violation = datetime.strptime(date_violation, "%Y-%m-%d").date() if date_violation else None

    department_user = await DepartmentUsersDAO.add(db, name=department)

    user = await UsersDAO.add(db, surname=surname, name=name, last_name=last_name,
                              department_id=department_user.id,
                       hired=hired_date, dismissal=dismissal_date)
    violation = await ViolationsDAO.add(db, type_violation=type_violation, date_violation=date_violation, tags=tags,
                        description=description, user_id=user.id)
    # Создаем и сохраняем эмбеддинг для нарушения
    await embed_one_violation(db, violation.id)

    files = None
    if not uploaded_files or not uploaded_files.filename:

        files = None
    else:
        filename = os.path.basename(uploaded_files.filename)
        upload_dir = "app/static/files"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)

        async with aiofiles.open(file_path, "wb") as f:
            content = await uploaded_files.read()
            await f.write(content)

 
        files = await UploadedFilesDAO.add(db, user_id=user.id, filename=filename, filepath=file_path)







    departments_dict = {department.name: department.value for department in Departments}
    department = departments_dict.get(department)
    violations_dict = {violation.name: violation.value for violation in TypeViolation}
    type_violation = violations_dict.get(type_violation)

    return templates.TemplateResponse("get_input_user.html", {"request": request, "user": user,
                                                              "department": department, "violation": violation,
                                                              "type_violation": type_violation,
                                                               "files": files})
