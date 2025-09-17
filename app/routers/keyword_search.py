from typing import Annotated

from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_depends import get_db
from app.servise.violations_search import semantic_search_violations

router = APIRouter(prefix="/keyword_search", tags=["keyword_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], keyword: str = Query(...)):
    """
    Семантический поиск нарушений
    :param request:
    :param db:
    :param keyword: поисковый запрос
    :return:
    """
    # Используем семантический поиск вместо простого keyword поиска
    rows = await semantic_search_violations(db, keyword, k=20)

    return templates.TemplateResponse("get_search.html", {"request": request, "rows": rows, "q": keyword})
