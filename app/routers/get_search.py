from typing import Annotated

from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession



from app.database.db_depends import get_db

from app.servise.violations_search import semantic_search_violations



router = APIRouter(prefix="/get_search", tags=["get_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)], query: str = Query(...)):
    rows = await semantic_search_violations(db, query, k=20)
    return templates.TemplateResponse("get_search.html", {"request": request, "rows": rows, "q": query})



