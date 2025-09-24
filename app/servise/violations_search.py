from sqlalchemy import text, bindparam
from sqlalchemy.ext.asyncio import AsyncSession
from pgvector.sqlalchemy import Vector
from app.models.models import Violations
from app.servise.embeddings import encode_query
from app.dao.dao import ViolationsDAO

async def embed_one_violation(db: AsyncSession, violation_id: int) -> None:
    """Создает эмбеддинг для одного нарушения и сохраняет его в базе данных"""
    # Получаем нарушение из базы данных
    violation = await ViolationsDAO.get_by_id(db, violation_id)
    if not violation or not violation.description:
        return

    # Создаем эмбеддинг для описания нарушения
    embedding = await encode_query(violation.description)

    # Обновляем нарушение с эмбеддингом
    await ViolationsDAO.update(db, violation_id, embedding=embedding)

async def semantic_search_violations(
    db: AsyncSession,
    query: str,
    k: int = 20,
    min_score: float = 0.6
) -> list[dict]:
    # Получаем эмбеддинг запроса (список чисел)
    qvec = await encode_query(query)

    stmt = text(f"""
        SELECT v.id AS violation_id,
               v.description,
               v.date_violation,
               u.id AS user_id,
               u.surname, u.name, u.last_name,
               1 - (v.embedding <=> CAST(:qvec AS vector)) AS score
        FROM {Violations.__tablename__} AS v
        JOIN users u ON u.id = v.user_id
        WHERE v.embedding IS NOT NULL
          AND (1 - (v.embedding <=> CAST(:qvec AS vector))) >= :min_score
        ORDER BY v.embedding <=> CAST(:qvec AS vector)
        LIMIT :k
    """).bindparams(
        bindparam("qvec", qvec, type_=Vector(len(qvec))),
        bindparam("min_score", min_score),
        bindparam("k", k),
    )

    rows = (await db.execute(stmt)).mappings().all()
    return [
        {
            "violation_id": r["violation_id"],
            "user_id": r["user_id"],
            "surname": r["surname"],
            "name": r["name"],
            "last_name": r["last_name"],
            "description": r["description"],
            "date_violation": r["date_violation"],
            "score": float(r["score"]),
        } for r in rows
    ]