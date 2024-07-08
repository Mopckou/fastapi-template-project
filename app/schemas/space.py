from pydantic import BaseModel, Field

from app.entities.space import SpaceEntity
from app.schemas.base import BaseResponse


class SpaceRequest(BaseModel):
    path: str = Field(..., title="Ссылка где создать пространство")
    name: str = Field(..., title="Имя пространства")
    slug: str = Field(..., title="Slug пространства")


class NewSpaceID(BaseModel):
    id: int = Field(..., title="Идентификатор пространства")


class NewSpaceResponse(BaseResponse):
    result: NewSpaceID


class SpaceResponse(BaseResponse):
    result: SpaceEntity | None


class SpaceResponses(BaseResponse):
    result: list[SpaceEntity]
