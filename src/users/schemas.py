from pydantic import BaseModel
from pydantic import EmailStr

from users.models import GroupEnum


class GroupBaseSchema(BaseModel):
    name: GroupEnum


class GroupResponseSchema(GroupBaseSchema):
    id: int

class UserBaseSchema(BaseModel):
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str
    group: str = "user"


class UserReadSchema(UserBaseSchema):
    id: int
    group_id: int

    class Config:
        from_attributes = True


class TokenBaseSchema(BaseModel):
    access_token: str
    token_type: str


class UserRegistrationResponseSchema(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

