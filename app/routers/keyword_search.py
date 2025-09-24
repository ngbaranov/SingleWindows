from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.dao.dao import UsersDAO, ViolationsDAO, DepartmentUsersDAO
from app.database.db_depends import get_db
from app.models.models import User, Violations
from app.models.sql_enums import Departments, TypeViolation
from app.servise.violations_search import semantic_search_violations

router = APIRouter(prefix="/keyword_search", tags=["keyword_search"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def get_search(request: Request, db: Annotated[AsyncSession, Depends(get_db)],
                     keyword: str = Query(...),
                     search_type: str = Query("keyword", description="keyword или semantic"),
                     k: int = Query(10, description="Количество результатов"),
                     min_score: float = Query(0.5, description="Минимальный порог релевантности для семантического поиска (0.0-1.0)")):
    """
    Поиск по ключевым словам или семантический поиск
    :param request:
    :param db:
    :param keyword:
    :param search_type: keyword или semantic
    :param k: Количество результатов
    :param min_score: Минимальный порог релевантности для семантического поиска
    :return:
    """
    if search_type == "semantic":
        # Семантический поиск с пороговым значением
        rows = await semantic_search_violations(db, keyword, k, min_score)
    else:
        # Обычный поиск по ключевым словам
        stmt = select(User).join(Violations).where(
            Violations.description.ilike(f"%{keyword}%")
        ).options(joinedload(User.violations))

        result = await db.execute(stmt)
        users = result.unique().scalars().all()

        rows = []
        for user in users:
            for violation in user.violations:
                if violation.description and keyword.lower() in violation.description.lower():
                    rows.append({
                        "user_id": user.id,
                        "surname": user.surname,
                        "name": user.name,
                        "last_name": user.last_name,
                        "full_name": f"{user.surname} {user.name} {user.last_name}",
                        "description": violation.description,
                        "date_violation": violation.date_violation,
                        "score": 1.0
                    })

    return templates.TemplateResponse("get_search.html", {
        "request": request,
        "rows": rows,
        "q": keyword,
        "search_type": search_type
    })
