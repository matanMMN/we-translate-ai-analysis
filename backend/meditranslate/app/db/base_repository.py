from typing import Type, TypeVar, Generic, List, Optional, Any, Dict,Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import func, and_

from meditranslate.app.db.base import Base
from meditranslate.app.shared.schemas import GetManySchema, SortOrder
from meditranslate.app.errors import AppError, ErrorSeverity, HTTPStatus, ErrorType

from functools import reduce
from typing import Any, Generic, Type, TypeVar, List, Tuple, Optional

from sqlalchemy import Select, func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from meditranslate.app.loggers import logger

from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.relationships import RelationshipProperty

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base class for data repositories."""

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self.session = db_session
        self.model_class: Type[ModelType] = model
        if not db_session:
            raise AppError(title="WE NEED DB SESSION",http_status=HTTPStatus.INTERNAL_SERVER_ERROR)

    async def create(self, attributes: dict[str, Any] = None) -> ModelType:
        try:
            logger.debug(attributes)
            if attributes is None:
                attributes = {}
            else:
                attributes.pop("id",None)
                attributes.pop("created_at",None)
                attributes.pop("updatd_at",None)

            """Creates the model instance."""
            if attributes is None:
                attributes = {}
            model = self.model_class(**attributes)
            self.session.add(model)
            await self.session.flush()
            return model
        except Exception as e:
            logger.error(f"Error creating model instance: {e}")
            raise

    async def update(self, model_instance: ModelType, attributes: dict[str, Any]) -> ModelType:
        """
        Updates the model instance with the given attributes and refreshes it.

        Args:
            model_instance (ModelType): The model instance to be updated.
            attributes (dict[str, Any]): A dictionary of attributes to update.

        Returns:
            ModelType: The updated model instance.
        """

        try:
            for key, value in attributes.items():
                setattr(model_instance, key, value)
                print(key, value)
            await self.session.flush()
        except SQLAlchemyError as e:
            raise AppError(
                error=e,
                title="Database Error",
                description="An error occurred while updating the record",
                context="repository",
            ) from e

    async def get_all(self, skip: int = 0, limit: int = 100, joins: set[str] | None = None) -> list[ModelType]:
        """Returns a list of model instances."""
        query = self.build_query(joins=joins).offset(skip).limit(limit)
        try:
            return await self.fetch_all(query)
        except SQLAlchemyError as e:
            raise AppError(
                error=e,
                title="Database Error",
                description="Error occurred during get_all",
                context="repository",
            ) from e

    async def get_by(self, field: str, value: Any, joins: set[str] | None = None, unique: bool = False) -> ModelType:
        """Returns the model instance matching the field and value."""
        # results = self.session.execute(
        #     select(self.model_class).where(getattr(self.model_class,field) == value)
        # )
        logger.debug(f"Building query for field: {field} with value: {value}")
        query = await self.add_filter(self.build_query(joins=joins), field, value)
        return await (self.fetch_one(query) if unique else self.fetch_all(query))

    async def delete(self, model: ModelType) -> None:
        """Deletes the model."""
        try:
            await self.session.delete(model)
            await self.session.flush()
        except SQLAlchemyError as e:
            raise AppError(
                error=e,
                title="Database Error",
                description="Error occurred during delete",
                context="repository",
                http_status=HTTPStatus.NOT_FOUND
            ) from e

    def build_query(self, joins: Optional[set[str]] = None, order: Optional[dict] = None) -> Select:
        """Builds a query for the model, applying joins and ordering if provided."""
        query = select(self.model_class)
        query = self.apply_joins(query, joins)
        query = self.apply_ordering(query, order)
        return query

    async def get_many(self, filters: dict[str, Any] = None, sort_by: str = None, sort_order: str = "asc", offset: int = 0, limit: int = 100) -> Tuple[List[ModelType], int]:
        """Returns multiple model instances with filtering, sorting, and pagination."""
        try:
            query = self.build_query()
            if filters and filters is not None and filters !=  "":
                query = self.apply_filters(query, filters)
            if sort_by:
                query = await self.add_sort(query, sort_by, sort_order)

            query = query.offset(offset).limit(limit)
            total_count = await self.count(query)
            results = await self.fetch_all(query)

            return results, total_count

        except SQLAlchemyError as e:
            raise AppError(
                error=e,
                title="Database Error",
                description="Error occurred during get_many",
                context="repository",
            ) from e

    async def fetch_all(self, query: Select) -> list[ModelType]:
        """Executes the query and returns all results."""
        result = await self.session.scalars(query)
        return result.all()

    async def fetch_one(self, query: Select) -> ModelType:
        """Executes the query and returns a single result, raising if not found."""
        result = await self.session.scalars(query)
        return result.one_or_none()

    async def count(self, query: Select) -> int:
        """Returns the count of the records in the query."""
        count_query = query.subquery()
        result = await self.session.scalars(select(func.count()).select_from(count_query))
        return result.one()

    async def add_sort(self, query: Select, sort_by: str, order: str = "asc") -> Select:
        """Adds sorting to the query by the specified column and order."""
        order_column = getattr(self.model_class, sort_by)
        return query.order_by(order_column.desc() if order == "desc" else order_column.asc())

    async def add_filter(self, query: Select, field: str, value: Any) -> Select:
        """Adds a filter condition to the query by field and value."""
        return query.where(getattr(self.model_class, field) == value)

    def apply_joins(self, query: Select, joins: Optional[set[str]] = None) -> Select:
        """Applies join clauses to the query if joins are specified."""
        if joins:
            query = reduce(self.add_join, joins, query)
        return query

    def apply_ordering(self, query: Select, order: Optional[dict] = None) -> Select:
        """Applies ordering to the query if specified."""
        if order:
            if "asc" in order:
                for field in order["asc"]:
                    query = query.order_by(getattr(self.model_class, field).asc())
            if "desc" in order:
                for field in order["desc"]:
                    query = query.order_by(getattr(self.model_class, field).desc())
        return query

    def apply_filters(self, query: Select, filters: dict[str, Any]) -> Select:
        """Applies a set of filters to the query."""
        filter_conditions = [getattr(self.model_class, field) == value for field, value in filters.items()]
        return query.where(and_(*filter_conditions))

    def add_join(self, query: Select, join_: str) -> Select:
        """Applies a specific join to the query based on a join string."""
        return getattr(self, f"_join_{join_}")(query)
