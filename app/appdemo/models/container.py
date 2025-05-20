import logging

import dill
from django.db import models
from pydantic import validate_call

from appdemo.dataclasses.document import Chunk, Chunks
from appdemo.models.base import BaseAutoDate, BaseUUID
from appdemo.models.resource import Resource

logger = logging.getLogger(__name__)


def chunks_validator(chunks: list[dict] | None) -> None:
    """
    Validate that all chunks are dictionaries with the required keys.
    """
    if chunks is not None:
        Chunks.model_validate(chunks)
    return


class BaseChunkContainer(models.Model):
    """
    Class to store a group of ResourceChunkComponent in sequence.
    Stores the order of chunks using an intermediate model.

    Attributes:
        chunks_json: JSON field to store chunks of text
        chunks_file: FileField to store chunks of text combined by resource

    Properties:
        chunks: list[Chunk]: Get the chunks of the content in dataclass
    """

    chunks_json = models.JSONField(validators=[chunks_validator], null=True, blank=True)

    @property
    def chunks(self) -> list[Chunk]:
        """
        Get the chunks of the content in dataclass
        """
        if self.chunks_json:
            return Chunks(self.chunks_json).root
        raise ValueError("Chunks are not set.")

    @chunks.setter
    @validate_call
    def chunks(self, chunks: list[Chunk]):
        """
        Set the chunks of the content in dataclass
        """
        self.chunks_json = Chunks(chunks).model_dump()

    class Meta:
        abstract = True


class Page(BaseAutoDate, BaseUUID, BaseChunkContainer):
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
    )
    page_number = models.IntegerField()


class ChunkGroup(BaseAutoDate, BaseUUID, BaseChunkContainer):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    vector_binary = models.BinaryField(null=True, blank=True)

    @property
    def vector(self) -> list[float]:
        """
        Get the vector
        """
        if self.vector_binary:
            return dill.loads(self.vector_binary)
        raise ValueError("Vector is not set.")

    @vector.setter
    @validate_call
    def vector(self, vector: list[float]):
        """
        Set the vector
        """

        self.vector_binary = dill.dumps(vector)
