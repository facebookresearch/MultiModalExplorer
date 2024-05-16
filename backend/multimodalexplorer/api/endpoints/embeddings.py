# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.


import logging

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from multimodalexplorer.functions.fetch_embed import fetch_embeds, fetch_embeds_details
from multimodalexplorer.types.route_types import (
    EmbeddingsDetailsRequest,
    EmbeddingsDetailsResponse,
    EmbeddingsResponse,
)

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/get_embeddings", response_model=EmbeddingsResponse)
async def get_embeddings():

    try:
        embeddings = fetch_embeds()
        return EmbeddingsResponse(data=embeddings)

    except Exception as e:
        if isinstance(e, ValidationError):
            logger.error("Validation error on loading embeddings")
        else:
            logger.error(f"Failed to load embeddings: {str(e)}")

        raise HTTPException(
            status_code=500, detail=f"Failed to load embeddings: {str(e)}"
        )


@router.post("/get_embeddings_details", response_model=EmbeddingsDetailsResponse)
async def get_embeddings_details(embed_points: EmbeddingsDetailsRequest):

    try:
        embeddings_details = fetch_embeds_details(embed_points.points)
        return EmbeddingsDetailsResponse(data=embeddings_details)

    except Exception as e:
        if isinstance(e, ValidationError):
            logger.error("Validation error on loading embeddings details")
        else:
            logger.error(f"Failed to load embeddings details: {str(e)}")

        raise HTTPException(
            status_code=500, detail=f"Failed to load embeddings details: {str(e)}"
        )
