from logging import getLogger
from pprint import pprint  # noqa

from ninja import Router
from ninja.responses import codes_4xx

from appdemo.serializers.search_schema import ErrorOut, SearchPostIn, SearchPostOut

router = Router(tags=["Search"])

logger = getLogger(__name__)


@router.post(
    "/search/",
    response={200: SearchPostOut, codes_4xx: ErrorOut},
)
def test_search(
    request,
    payload: SearchPostIn,
):
    # Task: implement search feature using elasticsearch, pre-filter with the given resource_ids
    print(
        {
            "page": payload.resource.page_set.first(),
            "chunk_group": payload.resource.chunkgroup_set.first(),
        }
    )
    return {"query": payload.query, "resource": payload.resource, "data": None}
