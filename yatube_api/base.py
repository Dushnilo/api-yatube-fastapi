from sqlalchemy import select, insert, update, func
from sqlalchemy.orm import joinedload

from database import async_session_maker

from config import settings


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, *options, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)

            for option in options:
                query = query.options(joinedload(getattr(cls.model, option)))

            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, *options, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)

            for option in options:
                query = query.options(joinedload(getattr(cls.model, option)))

            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def find_all_with_pagination(
        cls,
        *options,
        offset: int = 0,
        limit: int = settings.PAGINATION_DEFAULT_LIMIT,
        **filter_by
    ):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .offset(offset)
                .limit(limit)
            )

            for option in options:
                query = query.options(joinedload(getattr(cls.model, option)))

            result = await session.execute(query)
            return result.unique().scalars().all()

    @classmethod
    async def get_total_count(cls):
        async with async_session_maker() as session:
            query = select(func.count()).select_from(cls.model)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add(cls, *options, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()

            added_record = result.scalar_one()

            if options:
                query = select(cls.model).filter_by(id=added_record.id)
                for option in options:
                    query = query.options(joinedload(getattr(cls.model,
                                                             option)))
                result = await session.execute(query)
                added_record = result.unique().scalar_one()

            return added_record

    @classmethod
    async def update(cls, model_id: int, *options, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(cls.model.id == model_id)
                .values(**data)
            )
            await session.execute(query)
            await session.commit()

            query = select(cls.model).where(cls.model.id == model_id)

            for option in options:
                query = query.options(joinedload(getattr(cls.model, option)))

            result = await session.execute(query)
            updated_instance = result.scalar_one_or_none()

            return updated_instance

    @classmethod
    async def delete(cls, model_id: int):
        async with async_session_maker() as session:
            post = await session.get(cls.model, model_id)
            await session.delete(post)
            await session.commit()
# 
