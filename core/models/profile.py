from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.models.base import Base
from core.models.mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = 'profile'

    first_name: Mapped[str | None] = mapped_column(String(32))
    last_name: Mapped[str | None] = mapped_column(String(32))
    bio: Mapped[str | None]


