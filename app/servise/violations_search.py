from typing import List, Dict, Any
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import Violations
from app.servise.embeddings import encode_passages, encode_query

def _payload_for_violation(v: Violations) -> str:
    """
    готовит единый текстовый контент,
    который потом отправляется в модель эмбеддингов
    :param v:
    :return: склеиная строка
    """
    parts = [
        (v.description or "").strip(),
        (v.tags or "").strip(),
        (v.type_violation.value if getattr(v, "type_violation", None) else "").strip(),
    ]
    parts = [p for p in parts if p]
    return " | ".join(parts)

async def embed_one_violation(db: AsyncSession, violation_id: int) -> None:
    """
    однократное построение эмбеддинга для конкретного нарушения
    :param db:
    :param violation_id:
    :return:
    """
    # асинхронно достаёт запись из таблицы violations по её primary key, если нет записи None.
    v = await db.get(Violations, violation_id)
    if not v:
        return
    # [vec] = ... — это распаковка: берём единственный элемент из списка, т.е. вектор именно для этого нарушения.
    [vec] = await encode_passages([_payload_for_violation(v)])
    # Устанавливаем в колонку embedding (в модели Violations) рассчитанный вектор.
    v.embedding = vec
    db.add(v)
    await db.commit()

async def bulk_embed_missing_violations(db: AsyncSession, batch_size: int = 200) -> int:
    """
    Пакетное построение эмбеддингов для нарушений, у которых embedding IS NULL.
    Берёт по batch_size записей, вычисляет для них эмбеддинги и сохраняет в БД.
    Возвращает общее число обработанных записей.
    :param db:
    :param batch_size:
    :return:
    """
    total = 0
    while True:
        ids = (await db.execute(
            select(Violations.id).where(Violations.embedding.is_(None)).limit(batch_size)
        )).scalars().all()
        if not ids:
            break

        records = (await db.execute(
            select(Violations).where(Violations.id.in_(ids))
        )).scalars().all()

        payloads = [_payload_for_violation(v) for v in records]
        vecs = await encode_passages(payloads)
        for v, emb in zip(records, vecs):
            v.embedding = emb
        db.add_all(records)
        await db.commit()
        total += len(records)
    return total

async def semantic_search_violations(db: AsyncSession, query: str, k: int = 20) -> list[dict]:
    qvec = await encode_query(query)

    tname = Violations.__tablename__  # ← возьмёт реальное имя (violations или violationss)
    stmt = text(f"""
        SELECT v.id AS violation_id,
               v.description,
               v.date_violation,
               u.id AS user_id,
               u.surname, u.name, u.last_name,
               1 - (v.embedding <=> :qvec) AS score
        FROM {tname} AS v
        JOIN users u ON u.id = v.user_id
        WHERE v.embedding IS NOT NULL
        ORDER BY v.embedding <=> :qvec
        LIMIT :k
    """)

    rows = (await db.execute(stmt, {"qvec": qvec, "k": k})).mappings().all()
    out = []
    for r in rows:
        out.append({
            "violation_id": r["violation_id"],
            "user_id": r["user_id"],
            "surname": r["surname"],
            "name": r["name"],
            "last_name": r["last_name"],
            "description": r["description"],
            "date_violation": r["date_violation"],
            "score": float(r["score"]),
        })
    return out