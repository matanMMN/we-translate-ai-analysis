from pydantic import BaseModel as PydanticBaseModel, Field,ConfigDict, PrivateAttr,model_validator
from meditranslate.app.shared.constants import SortOrder
from meditranslate.app.shared.base_schema import BaseSchema
from pydantic import BaseModel
from typing import Optional,Dict,Any,List


class PaginationSchema(BaseModel):
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class MetaSchema(BaseModel):
    pagination: Optional[PaginationSchema] = None


class GetManySchema(BaseModel):
    model_config:ConfigDict = ConfigDict(
        from_attributes=True
    )
    offset: Optional[int] = Field(default=0, ge=0)
    limit: Optional[int] = Field(default=None, ge=0)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = SortOrder.asc.value
    filters: Optional[Dict[str, Any] | str] = ""


class BaseResponseSchema(BaseModel):
    data: Optional[Any] = None  # When returning actual data
    message: Optional[str] = None  # Success or info message
    error: Optional[str] = None  # Error message in case of failure
    status_code: Optional[int] = Field(default=200, description="HTTP status code")
    meta: Optional[MetaSchema] = None  # Metadata, often for pagination
    warnings: Optional[List[str]] = None  # Warnings or additional information


