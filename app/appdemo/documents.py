from elasticsearch.dsl import Document, field

from appdemo.models.container import ChunkGroup, Page
from appdemo.models.resource import Resource


class BaseResourceDocument(Document):
    resource = field.Object(
        properties={
            "id": field.Keyword(),
            "name": field.Text(),
            "type": field.Text(),
        }
    )

    # @classmethod
    # def generate_id(cls, instance):
    #     return str(instance.id)  # type: ignore

    def prepare_resource(self, instance: Resource):
        return {
            "id": str(instance.id),
            "name": instance.name,
            "type": instance.type,
        }


class PageDocument(BaseResourceDocument):
    chunks = field.Nested(
        properties={
            "id": field.Keyword(),
            "en": field.Text(
                # Create custom analyzer for English text
            ),
            "ja": field.Text(
                # Create custom analyzer for Japanese text
            ),
        },
    )

    def prepare_chunks(self, instance: Page):
        # Complete this
        raise NotImplementedError("Chunks preparation is not implemented.")

    class Index:
        name = "page"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}


class ChunkGroupDocument(BaseResourceDocument):
    """Elasticsearch document for ResourceChunkGroupComponent"""

    chunks = field.Nested(
        properties={
            "id": field.Keyword(),  # Stores a single string without tokenization
            "page_number": field.Integer(),
            "en": field.Text(
                # Create custom analyzer for English text
            ),
            "ja": field.Text(
                # Create custom analyzer for Japanese text
            ),
        },
    )
    vector = field.DenseVector(
        dims=1536,
        similarity="cosine",
        index_options={
            "type": "hnsw",
            "m": 8,
            "ef_construction": 800,
        },
    )

    def prepare_chunks(self, instance: ChunkGroup):
        raise NotImplementedError("Chunks preparation is not implemented.")

    def prepare_vector(self, instance: ChunkGroup):
        return instance.vector
