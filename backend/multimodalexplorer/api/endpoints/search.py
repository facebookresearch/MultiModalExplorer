# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from multimodalexplorer.functions.search_faiss_index import SearchFaissIndex
from multimodalexplorer.utils.utils import select_params


def create_search_router(args: Dict[str, Any]) -> APIRouter:
    router = APIRouter()

    @router.post("/search_data")
    async def get_search_result(request: Request) -> Dict[str, Any]:

        data = await request.json()

        if "search_data" not in data or "search_type" not in data:
            return {"error": "Missing required fields 'search_data' or 'search_type'"}

        search_query = {
            "search_data": data["search_data"],
            "search_type": data["search_type"],
            "search_src_lang": data.get("search_src_lang", "eng_Latn"),
        }

        try:
            params = select_params(args, ["index_file", "raw_data_file", "index_args"])

            search = SearchFaissIndex(*params)
            search_result = search.process(search_query)

            return JSONResponse(content={"data": search_result}, status_code=200)
        except Exception as e:
            return {"error": f"Failed to search index: {str(e)}"}

    return router
