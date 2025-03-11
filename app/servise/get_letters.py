from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import User


async def get_available_letters(session: AsyncSession):
    result = await session.execute(select(func.left(User.surname, 1)).distinct())
    letters = result.scalars().all()
    return sorted(set(letter[0].upper() for letter in letters if letter[0]))