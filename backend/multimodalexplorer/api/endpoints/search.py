# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from multimodalexplorer.functions.search_faiss_index import SearchFaissIndex
from multimodalexplorer.types.route_types import SearchRequest, SearchResponse

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/search_data", response_model=SearchResponse)
async def get_search_result(search_request: SearchRequest) -> dict:

    try:
        search = SearchFaissIndex()
        search_result = search.process(search_request.model_dump())

        return SearchResponse(data=search_result)
    except Exception as e:
        if isinstance(e, ValidationError):
            logger.error("Validation error on search index")
        else:
            logger.error(f"Failed to search index: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search index: {str(e)}")
