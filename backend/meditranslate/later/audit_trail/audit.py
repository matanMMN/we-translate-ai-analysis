from sqlalchemy import Integer, String, Text, DateTime, ForeignKey,JSON
from sqlalchemy.orm import relationship,Mapped,mapped_column
from meditranslate.app.db import Base
from sqlalchemy.sql import func

class AuditTrail(Base):
    __tablename__ = 'audit_trails'

    table_name = Column(String(255), nullable=False)

    file_size: Mapped[float] = mapped_column(Float, nullable=False)

    record_id = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    entity = Column(String(50), nullable=False)
    field_name = Column(String(255))
    old_value = Column(JSON)
    new_value = Column(JSON)

    changed_by = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    changed_by_user = relationship('User', foreign_keys=[changed_by])
