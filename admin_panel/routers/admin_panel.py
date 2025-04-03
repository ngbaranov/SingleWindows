from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO
from app.database.db_depends import get_db
from app.servise.get_letters import get_available_letters
from auth.service.current_user import get_current_admin_user

router = APIRouter(prefix="/admin_panel", tags=["admin_panel"])
templates = Jinja2Templates(directory="admin_panel/templates")


@router.get("/")
async def admin_panel(request: Request, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    users = await UsersDAO.get_all_users(db)
    available_letters = await get_available_letters(db)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "users": users, "available_letters": available_letters})