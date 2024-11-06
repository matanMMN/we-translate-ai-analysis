from typing import Any
from sqlalchemy.orm import DeclarativeBase,declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs
from .mixins.timestamp_mixin import TimestampMixin
from .mixins.id_mixin import IdMixin
from meditranslate.app.loggers import logger



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
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
