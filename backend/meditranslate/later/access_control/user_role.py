from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship,mapped_column,Mapped
from meditranslate.app.db import Base
from sqlalchemy.schema import UniqueConstraint

class UserRole(Base):
    __tablename__ = 'user_roles'
    __table_args__ = (
        UniqueConstraint('user_id','role_id', name='_user_role'),
        # UniqueConstraint('name','app_id', name='_name_app'),
    )
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE') , primary_key=True)
    role_id: Mapped[str] = mapped_column(ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)

    user: Mapped['User'] = relationship('User',foreign_keys=[user_id],back_populates="roles")
    role: Mapped['Role'] = relationship('Role',foreign_keys=[role_id],back_populates="users")

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id}, assigned_at={self.created_at})>"
