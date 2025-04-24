from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.dao.dao import UsersDAO, ViolationsDAO
from app.database.db_depends import get_db
from app.models.sql_enums import TypeViolation
from auth.service.current_user import get_current_admin_user

router = APIRouter(prefix="/edit_all", tags=["edit_all"])
templates = Jinja2Templates(directory=["app/templates", "admin_panel/templates"])


@router.get("/{id}")
async def get_edit_all(request: Request, id: int, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    user = await UsersDAO.get_user_by_id(db, id)
    return templates.TemplateResponse("edit_all.html", {"request": request, "user": user})


@router.post("/save_edit/{id}")
async def save_edit_user(
    id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    admin_user: dict = Depends(get_current_admin_user),
    surname: str = Form(...),
    name: str = Form(...),
    last_name: str = Form(...),
    hired: str = Form(None),
    dismissal: str = Form(None),
    violation_ids: list[int] = Form(...),

):
    # Получаем все остальные поля формы
    form_data = await request.form()

    hired_date = None
    dismissal_date = None

    if hired:
        try:
            hired_date = datetime.strptime(hired, "%Y-%m-%d").date()
        except ValueError:
            pass  # можно логировать

    if dismissal:
        try:
            dismissal_date = datetime.strptime(dismissal, "%Y-%m-%d").date()
        except ValueError:
            pass  # можно логировать

    # Обновляем пользователя (даты по-прежнему строки, если понадобятся — тоже можно конвертнуть)
    await UsersDAO.update(
        db,
        record_id=id,
        surname=surname,
        name=name,
        last_name=last_name,
        hired=hired_date,
        dismissal=dismissal_date
    )
    # Обновляем нарушения
    for i, v_id in enumerate(violation_ids):
        type_field = f"type_violation_{i}"
        date_field = f"date_violation_{i}"
        desc_field = f"description_{i}"

        type_violation_raw = form_data.get(type_field)
        date_violation_raw = form_data.get(date_field)
        description_raw = form_data.get(desc_field)

        # Преобразуем строку в Enum
        try:
            type_violation = TypeViolation(type_violation_raw)
        except ValueError:
            type_violation = TypeViolation.Access_mode

        # Преобразуем дату в datetime
        date_violation = None
        if date_violation_raw:
            try:
                date_violation = datetime.strptime(date_violation_raw, "%Y-%m-%d")
            except ValueError:
                date_violation = None

        await ViolationsDAO.update(
            db,
            record_id=v_id,
            type_violation=type_violation,
            date_violation=date_violation,
            description=description_raw
        )

    updated_user = await UsersDAO.get_user_by_id(db, id)

    return templates.TemplateResponse("user.html", {
        "request": request,
        "user": updated_user,
        "is_admin": True  # т.к. сюда может попасть только админ
    })
