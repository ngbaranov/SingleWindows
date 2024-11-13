from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.dao import UsersDAO
from app.database.db_depends import get_db

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def get_index(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    users = await UsersDAO.get_all_users(db)

    return templates.TemplateResponse("index.html", {"request": request, "users": users})