from itertools import batched

from litellm import embedding


def get_texts_embedding(
    model: str,
    text_list: list[str],
    batch_embedding_size: int = 256,
    **kwargs,
) -> list[list[float]]:
    """
    Get embedding vector of the given text using litellm's embedding function.

    for result format,
    see https://docs.litellm.ai/docs/embedding/supported_embedding#output-from-litellmembedding

    Returns:
        list[list[float]]
    """

    vectors: list[list[float]] = []
    for batch_texts in batched(text_list, batch_embedding_size):
        response = embedding(
            model=model,
            input=batch_texts,
            **kwargs,
        )
        vectors.extend(map(lambda elem: elem["embedding"], response.data)) # type: ignore
    return vectors