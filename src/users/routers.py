from urllib.error import HTTPError

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.dependencies import get_db
from users.crud import get_user_by_email, create_user_in_db, create_group_in_db
from users.models import Group
from users.schemas import UserCreateSchema, UserReadSchema, GroupResponseSchema, GroupBaseSchema

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/groups/",
             response_model=GroupResponseSchema,
             status_code=status.HTTP_201_CREATED
             )
async def create_group(
        group_data: GroupBaseSchema,
        db: AsyncSession = Depends(get_db)
):
    return await create_group_in_db(db=db, group=group_data)

@router.get("/groups/", response_model=list[GroupResponseSchema])
async def get_all_groups(
        db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(Group))
    groups = res.scalars().all()
    return groups


@router.get("/users/")
async def read_users():
    return {"message": "List of users"}


@router.post("/register",
            response_model = UserReadSchema,
            status_code=status.HTTP_201_CREATED
)
async def create_user(
        user_data: UserCreateSchema,
        db: AsyncSession = Depends(get_db)
):
    db_user = await get_user_by_email(email=user_data.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exist")

    result = await db.execute(select(Group).where(Group.name == user_data.group.upper()))
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    return await create_user_in_db(db=db, user=user_data, group_obj=group)
