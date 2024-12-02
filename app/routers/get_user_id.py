from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao.dao import UsersDAO
from app.database.db_depends import get_db



router = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/{id}")
async def get_user_id(request: Request, id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    user = await UsersDAO.get_user_by_id(db, id)
    return templates.TemplateResponse("user.html", {"request": request, "user": user})



