from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    # _user_id_nullable = False
    # _user_id_unique = False

    _user_back_populates = 'posts'
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )


    def __str__(self) -> str:
        return f'{self.__class__.__name__}: (id={self.id}, username={self.title!r}, author: {self.user_id})'

    def __repr__(self) -> str:
        return str(self)