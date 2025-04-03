from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import Response
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse

from app.database.db_depends import get_db
from app.dao.dao import AdminDAO
from auth.service.authenticate import authenticate_user
from auth.service.token_jvt import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory=["auth/templates", "app/templates", "admin_panel/templates"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





@router.get("/reg")
async def read_item(request: Request):
    title = "Главная страница"
    return templates.TemplateResponse("reg.html", {"request": request, "title": title})


@router.post("/forms")
async def create_user(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_db),
    username: str = Form(),
    password: str = Form()

):

    user = await AdminDAO.get_by_field(db, username=username)

    if user:
        answer = "Пользователь с таким именем уже существует"
        return templates.TemplateResponse(request=request, name="forms.html", context={"answer": answer})
    password = bcrypt_context.hash(password)
    new_user = await AdminDAO.add(db, username=username, password=password)
    new_token = await create_access_token(new_user.username, new_user.id, new_user.is_admin, expires_delta=timedelta(minutes=20))

    response = RedirectResponse(url="/admin_panel/", status_code=302)
    response.set_cookie(key='access_token', value=new_token, httponly=True)

    # answer = "Пользователь успешно создан"
    #
    # return templates.TemplateResponse(request=request, name="forms.html", context={"answer": answer})

    return response

@router.get("/login")
async def read_item(request: Request):
    title = "Авторизация"
    return templates.TemplateResponse("login.html", {"request": request, "title": title})


@router.post('/token')
# async def login(response: Response, request: Request, db: Annotated[AsyncSession, Depends(get_db)], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     token = await create_access_token(user.username, user.id, user.is_admin, expires_delta=timedelta(minutes=20))
#     response.set_cookie(key='access_token', value=token, httponly=True)
#     return templates.TemplateResponse(
#         "admin_panel.html",
#         {"request": request},
#         headers=response.headers  # Передаем заголовки с Set-Cookie
#     )
async def login(
    response: Response,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    token = await create_access_token(user.username, user.id, user.is_admin, expires_delta=timedelta(minutes=20))
    response = RedirectResponse(url="/admin_panel/", status_code=302)
    response.set_cookie(key='access_token', value=token, httponly=True)
    return response