from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_depends import get_db
from app.dao.dao import UsersDAO
from auth.service.current_user import get_current_admin_user

router = APIRouter(prefix="/delete_user", tags=["delete_user"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/{id}")
async def delete_user(id: int, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    # Удаляем пользователя по ID
    await UsersDAO.delete_by_id(db, id)

    # Выполняем редирект на главную страницу
    return RedirectResponse(url="/admin_panel", status_code=303)