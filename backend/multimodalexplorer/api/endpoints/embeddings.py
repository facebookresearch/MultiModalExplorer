# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


from typing import Any, Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from multimodalexplorer.functions.fetch_embed import fetch_embed


def create_embeddings_router() -> APIRouter:
    router = APIRouter()

    @router.get("/get_embeddings")
    async def get_embeddings() -> Dict[str, Any]:

        try:
            embeddings = fetch_embed()

            return JSONResponse(content={"data": embeddings}, status_code=200)
        except Exception as e:
            return {"error": f"Failed to load embeddings: {str(e)}"}

    return router
