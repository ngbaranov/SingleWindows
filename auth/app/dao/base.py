from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def get_users_with_details(cls,session: AsyncSession, *args):
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
                joinedload(cls.model.violations), joinedload(cls.model.files))
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


 