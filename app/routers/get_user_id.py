from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO
from app.database.db_depends import get_db
from admin_panel.service.header_admin_base import header_admin



router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory=["app/templates", "admin_panel/templates"])


@router.get("/{id}")
async def get_user_id(request: Request, id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await UsersDAO.get_user_by_id(db, id)
    # base_url = str(request.base_url)
    # is_admin = request.headers.get("Referer", "").startswith(f"{base_url}admin_panel/")
    is_admin = await header_admin(request)
    return templates.TemplateResponse("user.html", {"request": request, "user": user, "is_admin": is_admin})




