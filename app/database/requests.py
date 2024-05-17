from app.database.models import async_session
from app.database.models import User, Requirement
from sqlalchemy import select, update, delete, desc
from datetime import datetime


async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        elif user.name:
            return True
        return False


async def edit_user(tg_id, name, number, username=None):
    async with async_session() as session:
        user = await session.execute(
            update(User).where(User.tg_id == tg_id).values(name=name,
                                                           number=number,
                                                           username=username))
        await session.commit()


async def add_requirement(text, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Requirement(text=text,
                                user=user.id))
        await session.commit()


async def get_requirements():
    async with async_session() as session:
        requirements = await session.scalars(select(Requirement))
        return requirements


async def get_requirement(requirement_id):
    async with async_session() as session:
        requirement = await session.scalar(select(Requirement).where(Requirement.id == requirement_id))
        return requirement


async def get_user(u_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == u_id))
        return user


async def delete_requirement(requirement_id):
    async with async_session() as session:
        await session.execute(delete(Requirement).where(Requirement.id == requirement_id))
        await session.commit()
