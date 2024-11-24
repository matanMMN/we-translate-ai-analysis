from meditranslate.app.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.schema import UniqueConstraint
from typing import Optional, List

class Permission(Base):
    __tablename__ = 'permissions'
    __table_args__ = (
        UniqueConstraint('action','resource', name='_action_resource'),
        # UniqueConstraint('name','app_id', name='_name_app'),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)  # e.g., 'read', 'write', 'delete'
    action: Mapped[str] = mapped_column(String, nullable=True)  # e.g., 'read', 'write', 'delete'
    resource: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., 'user', 'file', 'report' default None = 'all'
    resource_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)  # e.g., 'user', 'file', 'report' default None = 'all'
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    roles: Mapped[List['RolePermission']] = relationship('RolePermission', back_populates='permission')

    def __repr__(self):
        return f"<Permission(id={self.id}, name={self.name})>"
