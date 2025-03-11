from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO
from app.database.db_depends import get_db
from auth.service.current_user import get_current_admin_user

router = APIRouter(prefix="/admin_panel", tags=["admin_panel"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def admin_panel(request: Request, db: Annotated[AsyncSession, Depends(get_db)], admin_user: dict = Depends(get_current_admin_user)):
    users = await UsersDAO.get_all_users(db)
    return templates.TemplateResponse("admin_panel.html", {"request": request, "users": users})