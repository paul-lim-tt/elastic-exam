from collections import defaultdict
from itertools import batched
from uuid import uuid4

import config
from lib.dataclasses.content import ExtractedContent
from lib.dataclasses.document import Chunk
from lib.models.container import ChunkGroup, Page
from lib.models.resource import Resource
from lib.modules.content import detect_language, fit_quadrilateral
from lib.services.embedding import get_texts_embedding


def prepare_data(resource: Resource, extracted_content: ExtractedContent):
    page_info: dict[int, dict] = dict()
    for page in extracted_content.pages:
        page_info[page.pageNumber] = {
            "width": page.width,
            "height": page.height,
            "unit": page.unit,
        }

    chunks_by_page: defaultdict[int, list[Chunk]] = defaultdict(list)
    for paragraph in extracted_content.paragraphs:
        bounding_region = paragraph.boundingRegions[0]
        page_number = bounding_region.pageNumber
        [x, y, w, h] = fit_quadrilateral(bounding_region.polygon)
        chunks_by_page[page_number].append(
            Chunk(
                id=str(uuid4()),
                text=paragraph.content,
                language=detect_language(paragraph.content),
                page_number=page_number,
                x=x,
                y=y,
                w=w,
                h=h,
            )
        )

    all_chunks: list[Chunk] = []
    for _page_number, chunks in sorted(chunks_by_page.items()):
        all_chunks.extend(chunks)

    return (
        generate_page(resource, chunks_by_page),
        generate_chunk_group(resource, all_chunks),
    )


def generate_page(
    resource: Resource,
    chunks_by_page: dict[int, list[Chunk]],
):
    return [
        Page(
            resource=resource,
            page_number=page_num,
            chunks=chunks,
        )
        for page_num, chunks in sorted(chunks_by_page.items())
    ]


def generate_chunk_group(
    resource: Resource,
    chunks: list[Chunk],
    fixed_chunk_size: int = 5,
):
    batched_chunks = list(map(list, batched(chunks, fixed_chunk_size)))

    # prepare texts
    texts = [
        "".join(map(lambda chunk: chunk.text, chunks)) for chunks in batched_chunks
    ]
    # embed texts
    # vectors = [np.random.rand(1536).tolist() for _ in range(len(texts))]
    vectors = get_texts_embedding(
        model=config.EMBEDDING_MODEL,
        text_list=texts,
        api_base=config.EMBEDDING_API_BASE,
        api_key=config.EMBEDDING_API_KEY,
        api_version=config.EMBEDDING_API_VERSION,
    )

    return [
        ChunkGroup(
            resource=resource,
            vector=vector,
            chunks=chunks,
        )
        for chunks, vector in zip(batched_chunks, vectors)
    ]
