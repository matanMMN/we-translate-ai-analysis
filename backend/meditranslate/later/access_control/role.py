from meditranslate.app.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from typing import List, Optional

class Role(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    users: Mapped[List['UserRole']] = relationship('UserRole', back_populates='role') # type: ignore
    permissions: Mapped[List['RolePermission']] = relationship('RolePermission', back_populates='role') # type: ignore

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name}) desc={self.description}>"
