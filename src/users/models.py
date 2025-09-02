import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime, func, Enum, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class GroupEnum(enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class GenderEnum(enum.Enum):
    MAN = "man"
    WOMAN = "woman"


class Group(Base):
    __tablename__ = "group"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[GroupEnum] = mapped_column(Enum(GroupEnum), nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="group")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashes_password: Mapped[str] = mapped_column("hashed_password", String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="users")

    profile: Mapped["Profile"] = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    gender: Mapped[Optional[GenderEnum]] = mapped_column(Enum(GenderEnum))
    date_of_birth: Mapped[Optional[Date]] = mapped_column(Date)
    info: Mapped[Optional[str]] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    user: Mapped[User] = relationship("User", back_populates="profile")

