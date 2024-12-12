from typing import Any
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase,declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from .mixins.timestamp_mixin import TimestampMixin
from .mixins.id_mixin import IdMixin
from meditranslate.app.loggers import logger
from datetime import datetime,date

class Base(AsyncAttrs,DeclarativeBase, IdMixin, TimestampMixin):
    __abstract__ = True
    __table_args__ = {}
    __mapper_args__ = {}

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "__tablename__"):
            raise NotImplementedError(f"Class '{cls.__name__}' must define a __tablename__ attribute")

        if not hasattr(cls, "__repr__") or cls.__repr__ is Base.__repr__:
            logger.warning(f"Class '{cls.__name__}' did not define a __repr__ method")


    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"

    def as_dict(self):
        # return {
        #     c.name: (str(getattr(self, c.name)) if getattr(self, c.name) is not None else None)
        #     for c in self.__table__.columns
        # }
        def handle_value(value):
            if isinstance(value, dict):
                # Preserve dictionaries as they are
                return value
            elif isinstance(value, datetime) or isinstance(value, date):
                # Preserve datetime objects and return as ISO formatted string
                return value.isoformat() if value is not None else None
            elif isinstance(value, str):
                # Strings remain unchanged
                return value
            elif isinstance(value, (int, float, bool)):
                # Convert basic types (int, float, bool) to string
                return str(value)
            elif isinstance(value, Enum):  # Add handling for Enum types
                return value.value
            else:
                # Handle other types by converting to string
                return str(value) if value is not None else None

        return {
            c.name: handle_value(getattr(self, c.name))
            for c in self.__table__.columns
        }
