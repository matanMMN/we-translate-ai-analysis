from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import uuid

class IdMixin:
    """Id Mixin Class"""
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(36),  # UUID as string representation (36 characters)
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
    )






