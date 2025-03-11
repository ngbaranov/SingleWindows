import os
import aiofiles
 
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession



from app.database.db_depends import get_db
from app.models.models import UploadedFile
from app.dao.dao import UploadedFilesDAO, UsersDAO

router = APIRouter(prefix="/input_violation", tags=["input_violation"])
templates = Jinja2Templates(directory="app/templates")
@router.post("/upload_file/{user_id}")
async def upload_file(request: Request, user_id: int, db: Annotated[AsyncSession, Depends(get_db)], uploaded_file: UploadFile = File(...)):


    # Сохранение файла на сервере
    upload_dir = "app/static/files"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, uploaded_file.filename)

    async with aiofiles.open(file_path, "wb") as f:
        content = await uploaded_file.read()
        await f.write(content)

    # Сохранение информации о файле в БД
    await UploadedFilesDAO.add(db, user_id=user_id, filename=uploaded_file.filename, filepath=file_path)
    user = await UsersDAO.get_user_by_id(db, user_id)
    return templates.TemplateResponse("user.html", {"request": request, "user": user})