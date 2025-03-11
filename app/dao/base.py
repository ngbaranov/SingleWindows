from sqlalchemy import select, and_, update, delete
from sqlalchemy.orm import joinedload, query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Violations, UploadedFile


class BaseDAO:
    model = None

    @classmethod
    async def get_all_users(cls, session: AsyncSession):
        # Создаем запрос для выборки всех пользователей
        query = select(cls.model)

        # Выполняем запрос и получаем результат
        result = await session.execute(query)

        # Извлекаем записи как объекты модели
        records = result.scalars().all()

        # Возвращаем список всех пользователей
        return records

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_users_with_details(cls, session: AsyncSession, *args):
        # query = (select(cls.model).options(joinedload(cls.model.department),  # Загружаем департамент пользователя
        #         joinedload(cls.model.violations)  # Загружаем нарушения пользователя
        #     )
        # )
        # Создаем базовый запрос
        query = select(cls.model)

        # Добавляем динамические связи через joinedload
        for relation in args:
            query = query.options(joinedload(relation))

        result = await session.execute(query)
        return result.scalars().unique().all()

    @classmethod
    async def get_user_by_id(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).where(cls.model.id == user_id).options(joinedload(cls.model.department),
                                                                         joinedload(cls.model.violations),
                                                                         joinedload(cls.model.files))
        result = await session.execute(query)
        return result.scalars().unique().one()

    @classmethod
    async def get_by_field(cls, session: AsyncSession, **filters):
        """Получить запись по одному или нескольким полям."""
        if not filters:
            raise ValueError("Необходимо указать хотя бы одно поле для поиска.")

        conditions = [getattr(cls.model, key) == value for key, value in filters.items()]
        query = select(cls.model).where(and_(*conditions))

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, session: AsyncSession, record_id: int, **values):
        """
        Обновляет запись в базе данных по её ID.

        :param session: Асинхронная сессия SQLAlchemy.
        :param record_id: ID записи, которую нужно обновить.
        :param values: Поля и их новые значения для обновления.
        :return: Обновлённая запись или None, если запись не найдена.
        """
        if not values:
            raise ValueError("Необходимо указать хотя бы одно поле для обновления.")

        try:
            # Создаем запрос на обновление
            query = (
                update(cls.model)
                .where(cls.model.id == record_id)
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )

            # Выполняем запрос
            await session.execute(query)
            await session.commit()

            # Получаем обновлённую запись

        except SQLAlchemyError as e:
            await session.rollback()
            raise e


    @classmethod
    async def delete_by_id(cls, session: AsyncSession, record_id: int):
        try:
            # Создаем запрос на удаление
            # Удаляем связанные записи в таблице violations
            await session.execute(delete(Violations).where(Violations.user_id == record_id))

            # Удаляем связанные записи в таблице UploadedFile
            await session.execute(delete(UploadedFile).where(UploadedFile.user_id == record_id))

            # Удаляем пользователя
            await session.execute(delete(cls.model).where(cls.model.id == record_id))

            # Выполняем запрос
            await session.commit()

        except SQLAlchemyError as e:
            await session.rollback()
            raise e

