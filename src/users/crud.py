from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.dependencies import get_db
from users.models import User, Group
from users.schemas import UserCreateSchema, UserReadSchema, GroupBaseSchema
from users.security import hash_password

async def create_group_in_db(
        group: GroupBaseSchema,
        db: AsyncSession
):
    db_group = Group(name=group.name)
    db.add(db_group)

    await db.commit()
    await db.refresh(db_group)
    return db_group


async def create_user_in_db(
        user: UserCreateSchema,
        group_obj: Group,
        db: AsyncSession
):
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        hashes_password=hashed_password,
        group=group_obj,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_email(
        email: str,
        db: AsyncSession
):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()