from datetime import datetime, date

from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.dao import UsersDAO
from app.database.db_depends import get_db

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
                          ):
    hired_date = datetime.strptime(hired, "%Y-%m-%d").date() if hired else None
    dismissal_date = datetime.strptime(dismissal, "%Y-%m-%d").date() if dismissal else None
    user = await UsersDAO.add(db, username=username, address=address, phone_number=phone_number,
                       department=department, hired=hired_date, dismissal=dismissal_date)
    return templates.TemplateResponse("get_input_user.html", {"request": request, "user": user})

