from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from core.models import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.user import User


class UserRelationMixin:
    _user_id_unique: bool = False
    _user_back_populates: str | None = None
    _user_id_nullable: bool = False

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('users.id'),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship(
            'User',
            back_populates=cls._user_back_populates,
        )