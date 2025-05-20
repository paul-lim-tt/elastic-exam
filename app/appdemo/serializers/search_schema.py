from typing import Any
from uuid import UUID

from appdemo.models.resource import Resource
from ninja import ModelSchema, Schema
from ninja.errors import HttpError


class ErrorOut(Schema):
    detail: str


class SearchPostIn(Schema):
    resource_id: UUID
    query: str

    @property
    def resource(self) -> Resource:
        """
        Get the resource object from the database.
        """
        try:
            return Resource.objects.prefetch_related("page_set", "chunkgroup_set").get(
                id=self.resource_id
            )
        except Resource.DoesNotExist:
            raise HttpError(404, "Resource not found")


class ResourceSchema(ModelSchema):
    class Config:
        model = Resource
        model_fields = "__all__"


class SearchPostOut(Schema):
    query: str
    resource: ResourceSchema
    data: Any
