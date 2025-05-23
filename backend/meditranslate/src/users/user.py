from __future__ import annotations
from meditranslate.app.db import Base
from sqlalchemy import UUID, ForeignKey, String, Boolean,LargeBinary,JSON,Enum,Date
from sqlalchemy.orm import Mapped, mapped_column,relationship
from typing import Optional,Dict
from datetime import date
from meditranslate.utils.user_role.user_role import UserRole


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    role: Mapped[Optional[UserRole]] = mapped_column(Enum(UserRole, native_enum=False), nullable=False, default=UserRole.TRANSLATOR)
    first_name: Mapped[Optional[str]] = mapped_column(String, nullable=True,default=None)
    last_name: Mapped[Optional[str]] = mapped_column(String, nullable=True,default=None)

    avatar: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True,default=None)  # Store image as BYTEA  | # avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # URL or path
    avatar_url:  Mapped[Optional[str]] = mapped_column(String, nullable=True,default=None)  # Store image as BYTEA  | # avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # URL or path

    last_login: Mapped[Optional[date]] = mapped_column(Date, nullable=True,default=None)
    is_disabled: Mapped[Optional[bool]] = mapped_column(Boolean,default=False)
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    additional_fields: Mapped[Optional[Dict]] = mapped_column(JSON, nullable=True, default=None)

    created_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id'),nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(ForeignKey('users.id'),nullable=True)

    created_by_user: Mapped[Optional['User']] = relationship('User',foreign_keys=[created_by], lazy='select', remote_side='User.id')
    updated_by_user: Mapped[Optional['User']] = relationship('User',foreign_keys=[updated_by], lazy='select',  remote_side='User.id')


    @property
    def full_name(self)-> Optional[str]:
        if self.first_name and self.last_name:
            return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
        elif self.first_name:
            return f"{self.first_name.capitalize()}"
        elif self.last_name:
            return f"{self.last_name.capitalize()}"
        else:
            return None

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

