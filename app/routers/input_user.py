from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import session_user

from app.models.models import User
from app.database.db import connection
from app.database.db_depends import get_db

from typing import Annotated


router = APIRouter(prefix="/input_user", tags=["input_user"])
templates = Jinja2Templates(directory="app/templates")
@connection
@router.get("/")
async def get_input_user(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return templates.TemplateResponse("input_user.html", {"request": request, "users": users})




