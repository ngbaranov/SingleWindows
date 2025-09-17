
import os, asyncio
from typing import List
import numpy as np

_model = None
_model_lock = asyncio.Lock()

async def get_model():
    """Ленивая, потокобезопасная загрузка SentenceTransformer (имя через EMB_MODEL)."""
    global _model
    if _model is None:
        # Ставим замок и если модель все еще None загружаем к кэш для одинарной загрузки
        async with _model_lock:
            if _model is None:
                name = os.getenv("EMB_MODEL", "intfloat/multilingual-e5-base")

                def _load():
                    from sentence_transformers import SentenceTransformer
                    return SentenceTransformer(name)

                loop = asyncio.get_running_loop()
                _model = await loop.run_in_executor(None, _load)
    return _model


async def encode_passages(texts: List[str]) -> List[list[float]]:
    """Кодируем документы/записи (passage: ...) → list[list[float32]].
    Берём список текстов. Добавляем к каждому префикс "passage: ".
    Отправляем их в модель для кодирования. Результат приводим к list[list[float32]].
    Работа выполняется в отдельном потоке, чтобы не мешать asyncio.
    """
    model = await get_model()

    def _work(items: List[str]) -> List[list[float]]:
        """model.encode(items, normalize_embeddings=True) — берёт список текстов и
         возвращает массив numpy (каждая строка → вектор размерности 768)."""
        vecs = model.encode(items, normalize_embeddings=True)
        # Каждый вектор преобразуем в float32 и превращаем в список
        return [v.astype(np.float32).tolist() for v in vecs]
    # Берём текущий event loop (главный цикл asyncio).
    loop = asyncio.get_running_loop()
    # Кодируем документ
    prefixed = ["passage: " + t for t in texts]
    # Функция возвращает список векторов
    return await loop.run_in_executor(None, _work, prefixed)


async def encode_query(text: str) -> list[float]:
    """Кодируем запрос (query: ...) → list[float32]."""
    model = await get_model()

    def _one(q: str) -> list[float]:
        """
        Кодируем строку в вектор
        :param q:
        :return:
        """
        v = model.encode(q, normalize_embeddings=True)
        return v.astype(np.float32).tolist()

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _one, "query: " + text)