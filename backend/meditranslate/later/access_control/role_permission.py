from typing import Optional
from meditranslate.app.db import Base
from sqlalchemy import ForeignKey,Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (
        UniqueConstraint('role_id','permission_id', name='_role_permission'),
        # UniqueConstraint('name','app_id', name='_name_app'),
    )

    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id", ondelete='CASCADE'), primary_key=True)
    permission_id: Mapped[str] = mapped_column(ForeignKey("permissions.id", ondelete='CASCADE'), primary_key=True)

    role: Mapped["Role"] = relationship("Role",foreign_keys=role_id,back_populates="permissions")
    permission: Mapped["Permission"] = relationship("Permission",foreign_keys=permission_id,back_populates="roles")


    def __repr__(self):
        return f"<RolePermission(role_id={self.role_id}, permission_id={self.permission_id})>"
